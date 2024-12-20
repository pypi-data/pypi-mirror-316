import numpy as np
import ctypes
import multiprocessing as mp
from typing import Callable, List, Tuple, Optional

def shmem_as_ndarray(raw_array: mp.RawArray) -> np.ndarray:
    """Convert a multiprocessing.RawArray to a NumPy ndarray."""
    ctypes_to_numpy = {
        ctypes.c_char: np.int8,
        ctypes.c_wchar: np.int16,
        ctypes.c_byte: np.int8,
        ctypes.c_ubyte: np.uint8,
        ctypes.c_short: np.int16,
        ctypes.c_ushort: np.uint16,
        ctypes.c_int: np.int32,
        ctypes.c_uint: np.uint32,
        ctypes.c_long: np.int32,
        ctypes.c_ulong: np.uint32,
        ctypes.c_longlong: np.int64,
        ctypes.c_float: np.float32,
        ctypes.c_double: np.float64,
    }
    numpy_dtype = ctypes_to_numpy[raw_array._type_]
    count = ctypes.sizeof(raw_array) // numpy_dtype().itemsize
    return np.frombuffer(raw_array, dtype=numpy_dtype, count=count)

class Scheduler:
    def __init__(self, input_slices: List[List[slice]], output_slices: List[List[slice]]):
        """
        Initialize scheduler with input and output slices.
        
        Args:
            input_slices: List of multidimensional slices for input arrays
            output_slices: List of corresponding output slices
        """
        if len(input_slices) != len(output_slices):
            raise ValueError("input_slices and output_slices must have the same length")
            
        self.input_slices = input_slices
        self.output_slices = output_slices
        self.n_cnt = mp.RawValue(ctypes.c_int, -1)
        self.lock = mp.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            if self.n_cnt.value < len(self.input_slices) - 1:
                self.n_cnt.value += 1
                idx = self.n_cnt.value
                return self.input_slices[idx], self.output_slices[idx]
            raise StopIteration

def parallel(nproc: int, 
            input_slices: List[List[slice]], 
            output_slices: Optional[List[List[slice]]] = None,
            shm_idx: List[int] = [0],
            out_type: Optional[np.dtype] = None):
    """
    Parallel processing decorator that uses predefined input and output slices.
    
    Args:
        nproc: Number of processes to use
        input_slices: List of multidimensional slices for input arrays
        output_slices: List of corresponding output slices. If None, uses input_slices
        shm_idx: Indices of arguments that should be treated as shared memory arrays
        out_type: Output data type (defaults to input type if None)
    """
    def wrapper(func: Callable):
        def inner(*args, **kwargs):
            nonlocal output_slices
            # If output_slices not provided, use input_slices
            actual_output_slices = output_slices if output_slices is not None else input_slices
            
            if nproc > 1:
                return mp_func(func, args, shm_idx, input_slices, actual_output_slices, nproc, out_type)
            return func(*args, **kwargs)
        return inner
    return wrapper

def mp_func(func: Callable, 
           args: Tuple, 
           shm_idx: List[int], 
           input_slices: List[List[slice]],
           output_slices: List[List[slice]], 
           nproc: int,
           out_type: Optional[np.dtype] = None):
    """Implementation of parallel processing using multiprocessing."""
    def go_parallel(scheduler: Scheduler, func: Callable, args: Tuple, shm_out: mp.RawArray, shm_idx: List[int]):
        """Worker function that processes data chunks in parallel."""
        for in_slc, out_slc in scheduler:
            _args = [arg if i not in shm_idx else arg[tuple(in_slc)] for i, arg in enumerate(args)]
            sub_out = func(*_args)
            try:
                shm_out[tuple(out_slc)] = sub_out
            except ValueError as e:
                raise ValueError(f"Output shape mismatch. Expected shape for slice {out_slc}, "
                               f"got array of shape {sub_out.shape}") from e

    args = list(args)
    nproc = min(nproc, len(input_slices))
    
    # Determine output type
    out_type = out_type or args[shm_idx[0]].dtype

    final_shape = []
    input_array = args[shm_idx[0]]
    for dim in range(len(output_slices[0])):
        # If all slices for this dimension are slice(None), use input shape
        if all(s[dim] == slice(None) for s in output_slices):
            final_shape.append(input_array.shape[dim])
        else:
            # Otherwise find maximum stop index from actual slices
            max_idx = max(s[dim].stop if s[dim].stop is not None else 0 for s in output_slices)
            final_shape.append(max_idx)
    final_shape = tuple(final_shape)

    # Create shared memory array for output
    shm_out = mp.RawArray(out_type.char, int(np.prod(final_shape)))
    a_out = shmem_as_ndarray(shm_out).reshape(final_shape)

    # Initialize scheduler with both input and output slices
    scheduler = Scheduler(input_slices, output_slices)

    # Create and start processes
    pool = [mp.Process(target=go_parallel, 
                      args=(scheduler, func, args, a_out, shm_idx)) 
            for _ in range(nproc)]

    for p in pool:
        p.start()
    for p in pool:
        p.join()

    return a_out
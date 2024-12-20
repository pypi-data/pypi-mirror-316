import numpy as np
from typing import List, Tuple
from ..config import is_parallel_enabled, get_num_workers

def _guess_area_res_len(data_array, axis1: int, axis2: int, patch_size: int, func, kwargs):
    """
    Determine the output size from the function application on a patch.
    """
    test_slice = [slice(None)] * len(data_array.shape)
    test_slice[axis1] = slice(0, patch_size)
    test_slice[axis2] = slice(0, patch_size)
    
    first_patch = data_array[tuple(test_slice)]
    
    # Apply function with axis parameter
    first_result = func(first_patch, axis=(axis1, axis2), **kwargs)
    
    if not isinstance(first_result, np.ndarray) or first_result.shape == ():
        return 1
        
    if len(first_result.shape) < 2:
        return 1
        
    if (first_result.shape[0] == patch_size and 
        first_result.shape[1] == patch_size):
        return "same"
    
    if first_result.shape[0] != first_result.shape[1]:
        raise ValueError("Function must return square patches")
        
    return first_result.shape[0]

def _create_area_slices(shape: Tuple[int, ...], axis1: int, axis2: int, patch_size: int, res_len) -> Tuple[List[List[slice]], List[List[slice]]]:
    """
    Create input and output slices for area-based parallel processing.
    Slices along axis 0 in chunks of 1000, plus two additional specified dimensions.
    
    Args:
        shape: Shape of the input array
        axis1: First dimension to split
        axis2: Second dimension to split
        patch_size: Size of patches for processing
        res_len: Output size for each patch. Either an integer for square output or "same" 
                to keep original patch size
        
    Returns:
        Tuple of (input_slices, output_slices)
    """
    # Calculate number of patches in each dimension
    n_patches1 = shape[axis1] // patch_size
    n_patches2 = shape[axis2] // patch_size
    
    # Determine output size per patch
    if res_len == "same":
        output_patch_size = patch_size
    else:
        output_patch_size = res_len
    
    # Create input and output slices
    input_slices = []
    output_slices = []
    
    # Iterate over all three dimensions
    for i in range(n_patches1):
        for j in range(n_patches2):
            # Input slice (full patch size)
            current_slice = [slice(None)] * len(shape)
            current_slice[axis1] = slice(i * patch_size, (i + 1) * patch_size)
            current_slice[axis2] = slice(j * patch_size, (j + 1) * patch_size)
            input_slices.append(current_slice)
            
            # Output slice (res_len size)
            out_slice = [slice(None)] * len(shape)
            out_slice[axis1] = slice(i * output_patch_size, (i + 1) * output_patch_size)
            out_slice[axis2] = slice(j * output_patch_size, (j + 1) * output_patch_size)
            output_slices.append(out_slice)
            
    return input_slices, output_slices


def _apply_by_area(self, dim1: str, dim2: str, func: callable, patch_size: int, res_len = "same", **kwargs):
    """
    Apply a function to patches of a CoreArray along two specified dimensions.
    Can run in parallel based on configuration.
    
    Args:
        dim1 (str): First dimension name (e.g., 'lat')
        dim2 (str): Second dimension name (e.g., 'lon')
        func (callable): Function to apply to each patch
        patch_size (int): Size of square patches
        **kwargs: Additional arguments to pass to func
    """
    dims = list(self.coords.keys())
    axis1 = dims.index(dim1)
    axis2 = dims.index(dim2)
    
    shape = self.shape
    if shape[axis1] % patch_size != 0 or shape[axis2] % patch_size != 0:
        raise ValueError(f"Dimensions {dim1} and {dim2} must be divisible by patch_size {patch_size}")
    
    if res_len is None:
        res_len = _guess_area_res_len(self.__array__(), axis1, axis2, patch_size, func, kwargs)
        
    if not (isinstance(res_len, int) or res_len == "same"):
        raise ValueError("res_len must be either an integer or 'same'")
    
    input_slices, output_slices = _create_area_slices(shape, axis1, axis2, patch_size, res_len)
    output_patch_size = patch_size if res_len == "same" else res_len
    
    def process_patch(data):
        result = func(data, axis=(axis1, axis2), **kwargs)
        # Reshape the result to match expected output dimensions
        if isinstance(result, np.ndarray):
            if result.ndim == 1:
                # Create new shape with singleton dimensions for axis1 and axis2
                new_shape = [1 if i in (axis1, axis2) else s 
                           for i, s in enumerate(data.shape)]
                new_shape[0] = len(result)  # Set the actual data length
                result = result.reshape(new_shape)
        return result
    
    if is_parallel_enabled() and get_num_workers() > 1:
        from coreframe.parallel import parallel
        
        @parallel(nproc=get_num_workers(), 
                 input_slices=input_slices,
                 output_slices=output_slices,
                 shm_idx=[0])
        def parallel_wrapper(patch_data):
            return process_patch(patch_data)
        
        result = parallel_wrapper(self.__array__())
    else:
        output_shape = list(shape)
        n_patches1 = shape[axis1] // patch_size
        n_patches2 = shape[axis2] // patch_size
        output_shape[axis1] = n_patches1 * output_patch_size
        output_shape[axis2] = n_patches2 * output_patch_size
        result = np.empty(output_shape, dtype=self.dtype)
        
        data_array = self.__array__()
        for in_slice, out_slice in zip(input_slices, output_slices):
            patch_data = data_array[tuple(in_slice)]
            processed_patch = process_patch(patch_data)
            result[tuple(out_slice)] = processed_patch
    
    new_coords = self.coords.copy()
    for dim, axis in [(dim1, axis1), (dim2, axis2)]:
        coord_values = self.coords[dim]
        n_patches = shape[axis] // patch_size
        
        if res_len == "same":
            new_values = coord_values
        else:
            patch_coords = np.array([
                np.mean(coord_values[i * patch_size:(i + 1) * patch_size])
                for i in range(n_patches)
            ])
            new_values = np.repeat(patch_coords, output_patch_size)
            
        new_coords[dim] = new_values
    
    result = result.view(type(self))
    result.coords = new_coords
    
    return result
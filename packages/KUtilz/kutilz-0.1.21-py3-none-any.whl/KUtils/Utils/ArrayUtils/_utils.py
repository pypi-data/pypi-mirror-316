import numpy as np
from KUtils.Typing import *

ArrayLike = Union[List, np.ndarray]

def flattend(array: ArrayLike) -> List:
    return np.array(array).reshape(-1).tolist()

def rmv_dup(array: ArrayLike) -> List:
    array = np.array(array)
    _, idx = np.unique(array, return_index=True)
    return array[np.sort(idx)].tolist()
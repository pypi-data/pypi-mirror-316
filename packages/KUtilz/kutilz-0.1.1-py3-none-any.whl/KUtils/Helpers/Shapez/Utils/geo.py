import numpy as np
import shapely

def xy_extremas(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array).reshape(-1, 2)
    return np.array(
        [[array[..., 0].min(), array[..., 1].min()],
         [array[..., 0].max(), array[..., 1].max()]]
    )


def dilate_xxyy(array: np.ndarray, factor: float = .2) -> np.ndarray:
    assert array.shape == (2, 2)
    shift = (array[1] - array[0]) * factor
    return np.array(
        [array[0] - shift,
         array[1] + shift]
    )

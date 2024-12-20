import cv2
from KUtils.Helpers.Shapez.Bases.NumpyWrapper import *
from KUtils.Typing import *
from .Backends import *

class KImage(NumpyWrapper):
    __datatype__ = np.uint8

    @property
    def height(self) -> int:
        return self._data.shape[0]

    @property
    def width(self) -> int:
        return self._data.shape[1]

    @property
    def channel(self) -> int:
        return self._data.shape[2]

    def __init__(self, data: Any):
        super().__init__(data)

    def show(self, wname: str = 'yeeter', backend = 'cv') -> None:
        if backend == 'cv':
            import cv2 as cv
            cv.imshow(wname, self._data)
            cv2.waitKey()
        elif backend == 'pillow':
            from PIL import Image
            Image.fromarray(self.ernal).show(wname)
        else:
            raise BackendInvalidError(backend)

    @classmethod
    def Black(cls, dim: Tuple[int, int], bg = (0, 0, 0)) -> Self:
        _dim = (dim[1], dim[0])

        return cls(
            np.full((*_dim, len(bg)), bg)
        )

    @classmethod
    def Open(cls, path: PathLike) -> Self:
        from PIL import Image
        return cls(np.array(Image.open(path)))
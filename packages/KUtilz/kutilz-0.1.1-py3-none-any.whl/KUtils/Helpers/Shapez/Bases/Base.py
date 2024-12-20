import numpy as np
from KUtils.Helpers.Shapez.Bases.NumpyWrapper import *
from .KImage import KImage
import KUtils.Helpers.Shapez.Utils as utilz

_DEFAULT_COLOR = (255, 255, 255)
_DEFAULT_BACKDROP = (0, 0, 0)

RGBColor = Tuple[int, int, int]
Dim2D = Tuple[int, int]

class DrawParams(TypedDict):
    name: NotRequired[str]
    name_color: NotRequired[str]
    color: NotRequired[RGBColor]
    thickness: NotRequired[float]

class BaseShape2D(NumpyWrapper):
    def __draw__(self, target: ndarray, **params: Unpack[DrawParams]) -> ndarray:
        raise NotImplementedError()

    @property
    def bounds(self) -> ndarray:
        raise NotImplementedError()

    def draw_on(self, target: np.ndarray, **params: Unpack[DrawParams]) -> np.ndarray:
        from PIL import ImageColor
        for k in ['color', 'name_color']:
            _c = params.get(k, _DEFAULT_COLOR)
            if isinstance(_c, str):
                _c = ImageColor.getrgb(_c)
            params[k] = _c
        return self.__draw__(target, **params)

    @final
    def drawn(self,
                 shape: Tuple[int, int] = None,
                 scale: float = .8,
                 bgcolor: RGBColor = _DEFAULT_BACKDROP,
                 **kwargs: Unpack[DrawParams]) -> KImage:
        if shape is None:
            bounds = self.bounds
            bounds = utilz.dilate_xxyy(self.bounds, scale)
            shape = (bounds[1] - bounds[0]).astype(int)

        image = KImage.Blank(shape, bgcolor)
        self.draw_on(target=image.ernal, **kwargs)
        return image




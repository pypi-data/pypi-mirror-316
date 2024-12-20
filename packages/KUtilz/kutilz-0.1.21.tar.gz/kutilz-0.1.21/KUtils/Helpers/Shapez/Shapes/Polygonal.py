from KUtils.Helpers.Shapez.Bases.Base import *
from KUtils.Helpers.Shapez.Bases.Base import _DEFAULT_COLOR
from KUtils.Helpers.Shapez.Bases.Mixins import *
from KUtils.Typing import *


class PolygonalShape(BaseShape2D, IsSequential):
    __shape_constraint__ = (-1, 2)

    @property
    def bounds(self) -> ndarray:
        return utilz.xy_extremas(self.ernal)

class Polyline(PolygonalShape):
    def __draw__(self, target: ndarray, **params: Unpack[DrawParams]) -> ndarray:
        import cv2 as cv
        pnts = self._data.astype(np.int32).reshape(1, -1, 2)
        color = params.get('color', _DEFAULT_COLOR)
        cv.polylines(target, pnts, False, color, thickness=params.get('thickness', 5))
        return target
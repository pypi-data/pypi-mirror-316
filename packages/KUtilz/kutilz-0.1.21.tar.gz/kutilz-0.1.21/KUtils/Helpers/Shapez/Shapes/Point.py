from .Polygonal import *

class Point2D(BaseShape2D):
    __shape_constraint__ = (2)

    def __draw__(self, target: ndarray, **params: Unpack[DrawParams]) -> ndarray:
        import cv2 as cv

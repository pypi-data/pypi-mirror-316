import numpy as np
from KUtils.Helpers.Shapez.Shapes.Polygonal import *
from .Utils import *

class Shapez:
    def __init__(self):
        self.polyline = Polyline
        self.__do_wrap()

    def __do_wrap(self):
        pass

    def draw(self,
             *args: BaseShape2D,
             shapes: Dict[BaseShape2D, DrawParams] = None,
             img: Union[str, np.ndarray] = None) -> KImage:
        if img is None:
            bounds = [shape.bounds for shape in all_shapes]
            final_bounds = xy_extremas(bounds)
            final_bounds = dilate_xxyy(final_bounds, 1)
            final_bounds = final_bounds[1] - final_bounds[0]

            img = KImage.Black(final_bounds.astype(int))
        else:
            if isinstance(img, np.ndarray):
                img = KImage(img)
            elif isinstance(img, (str, Path)):
                img = KImage.Open(img)
            else:
                raise TypeError(img)

        shapes = shapes or {}
        all_shapes: List[BaseShape2D] = (list(args) or []) + (list(shapes.keys()))

        for shape in all_shapes:
            shape.draw_on(img.ernal, **shapes.get(shape, {}))

        return img

    def show(self,
             *args: BaseShape2D,
             shapes: Dict[BaseShape2D, DrawParams] = None,
             img: Union[str, np.ndarray] = None) -> KImage:
        img = self.draw(*args, shapes=shapes, img=img)
        img.show()
        return img

shapez = Shapez()
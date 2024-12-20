import numpy as np
from numpy import ndarray
from KUtils.Typing import *

if TYPE_CHECKING:
    from torch import Tensor

class NumpyWrapper:
    __datatype__ = np.float32
    __shape_constraint__: list = None

    @property
    def ernal(self) -> ndarray:
        return self._data

    def __init__(self, data: Union[ndarray, list, 'Tensor']):
        _data = np.array(data, dtype=self.__datatype__)
        if self.__shape_constraint__ is not None:
            _data = np.reshape(_data, self.__shape_constraint__)
        self._data = _data

    def __getitem__(self, item):
        return self.__class__(self._data[item])

    def __array__(self, dtype: str = None, copy: bool = None):
        new = self._data
        if dtype != self._data.dtype:
            new = new.astype(dtype)

        if copy is True:
            raise NotImplementedError()

        return new
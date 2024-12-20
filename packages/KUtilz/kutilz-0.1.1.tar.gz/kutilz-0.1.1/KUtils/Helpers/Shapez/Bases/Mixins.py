import numpy

from KUtils.Typing import *

class IsSequential:
    _data: numpy.ndarray

    def _compute_sequence_len(self) -> int:
        return self._data.shape[0]

    @property
    def length(self) -> int:
        return self._compute_sequence_len()
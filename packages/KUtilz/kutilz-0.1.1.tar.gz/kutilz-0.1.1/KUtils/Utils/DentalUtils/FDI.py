from KUtils.Typing import *

def _teeth_upto(qudrant: int, upto: int)->List[int]:
    return [qudrant*10 + tooth_num for tooth_num in range(1, upto+1)]

def get_all(permanent=True,
            deciduous=False,
            supernumerary=False,
            dtype: Type[T] = int)->List[T]:
    fdis = []
    if permanent:
        for quadrant in range(1, 4 + 1):
            fdis.extend(_teeth_upto(quadrant, 8))

    if deciduous:
        for quadrant in range(5, 8 + 1):
            fdis.extend(_teeth_upto(quadrant, 5))

    fdis = [dtype(i) for i in fdis]

    return fdis

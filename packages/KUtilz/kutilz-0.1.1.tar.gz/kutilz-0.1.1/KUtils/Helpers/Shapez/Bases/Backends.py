from KUtils import Strenum

class BackendInvalidError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Backend {name} is not a valid one.')

class Bakend(Strenum):
    CV = 'cv'
    PILLOW = 'pillow'
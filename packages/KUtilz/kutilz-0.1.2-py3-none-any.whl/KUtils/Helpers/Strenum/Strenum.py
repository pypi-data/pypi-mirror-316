from enum import Enum

class Strenum(str, Enum):
    @classmethod
    def IsLegal(cls, value: str) -> bool:
        return value in cls
    pass
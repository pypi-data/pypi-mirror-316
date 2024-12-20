from inspect import signature
from KUtils.Typing import *

def return_of(fun: Callable[P, T]) -> Type[T]:
    sig = signature(fun)
    ret_type = sig.return_annotation
    if ret_type == sig.empty:
        return Any
    else:
        return ret_type

def of_attrs(obj: object, type: Type[T]) -> Dict[str, Type[T]]:
    ret = {}
    for attr, val in obj.__dict__:
        if isinstance(val, type):
            ret[attr] = val

    return ret


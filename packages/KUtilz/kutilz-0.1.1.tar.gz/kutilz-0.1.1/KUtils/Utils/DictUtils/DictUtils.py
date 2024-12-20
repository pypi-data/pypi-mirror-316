from typing import List, Any, TypeVar, Dict, Callable, Iterable, Optional

V = TypeVar('V')
K = TypeVar('K')
T = TypeVar('T')

def recursive_mut(
            d: Dict[K, Any],
            predicate: Callable[[Any], bool],
            mutter: Callable[[K, Any], Any],
            prefix: str = '') -> None:
    for key, val in d.items():
        if isinstance(val, dict):
            recursive_mut(val, predicate, mutter, prefix=prefix + f':{key}')
        elif predicate(val):
            d[key] = mutter(key, val)

def make_dicts(keys: List[str], vals: List[List[Any]])->dict:
    assert all([len(keys) == len(sub_vals) for sub_vals in vals])
    
    res = []
    for sub_val in vals:
        new_item = {}
        for i, key in enumerate(keys):
            new_item[key] = sub_val[i]

        res.append(new_item)
    return res

def merge(dict0: dict, dict1: dict)->dict:
    interm = dict0.copy()
    interm.update(dict1)
    return interm

def set_chained(dict: dict, keys: List[str], val: Any)->None:
    next = dict
    for key in keys[:-1]:
        if not key in next:
            next[key] = {}

        next = next[key]

    next[keys[-1]] = val

def get_chained(dict: dict, keys: List[str])->Any:
    next = dict
    for key in keys[:-1]:
        next = next[key]

    return next.get(keys[-1])

def auto_dict(*args)->dict:
    return dict({arg:eval(arg) for arg in args})

def vmap(d: Dict[K, V], func: Callable[[V], T])-> Dict[K, T]:
    return {
        key: func(val) for key, val in d.items()
    }

def kmap(d: Dict[K, V], func: Callable[[K], T])-> Dict[T, V]:
    return {
        func(key): val for key, val in d.items()
    }

def notin(a: dict, b: dict)->dict:
    return {
        key: val for key, val in a.items if key not in b.keys()
    }

def select(d: dict, keys: Iterable[Any]) -> dict:
    return {
        key: d[key] for key in keys
    }

def find_key_by_val(d: Dict[K, V], v: V) -> Optional[K]:
    for key, val in d.items():
        if val == v:
            return key

    return None

def invert(d: Dict[K, V]) -> Dict[V, K]:
    return {
        v: k for k, v in d.items()
    }
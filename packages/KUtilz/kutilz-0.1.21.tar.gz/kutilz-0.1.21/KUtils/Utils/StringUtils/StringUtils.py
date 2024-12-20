from KUtils.Typing import *
import re

def parse_eq_expr(expr: str):
    pair = expr.split('=')
    return pair[0], pair[1]

def all_indices(s: str, target: str)->List[int]:
    indices = [i for i, x in enumerate(s) if x == target]
    return indices

def rm(s: str, target: str)->str:
    return s.replace(target, '') if target in s else s

def rm_all(s: str, targets: List[str])->str:
    while len(targets) > 0:
        s = rm(s, targets.pop(0))
    return s

def parse_int(s: str)->Union[int, str]:
    try:
        return int(s)
    except ValueError as e:
        return s

def parse_dom_attribs(attribs: str, delim: str = ',')->Dict[str, str]:
    res = {}
    for items in attribs.split(delim):
        pair = items.split('=')
        res[pair[0]] = pair[1]
    
    return res

def split_capital(s: str) -> List[str]:
    return re.split('(?<=.)(?=[A-Z])', s)
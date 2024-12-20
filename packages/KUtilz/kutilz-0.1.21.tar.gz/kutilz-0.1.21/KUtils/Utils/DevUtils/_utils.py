from KUtils.Typing import *
import pkgutil

def generic_args(cls: type, count: int = None) -> List[Any]:
    if not isinstance(cls, type):
        cls = cls.__class__

    try:
        orig_bases = cls.__orig_bases__
    except AttributeError:
        orig_bases = [cls]
    params = []
    for base in orig_bases:
        params.extend([*typing.get_args(base)])

    if count is not None:
        assert len(params) == count
    return params


def force_list(obj: Union[T, List[T]]) -> List[T]:
    if isinstance(obj, list):
        return obj
    else:
        return [obj]
    
from importlib import import_module
import importlib
def from_import(module_res: str, obj_name: str, default=None, local=False)->Any:
    module = import_module(module_res, package='.' if local else None)
    return getattr(module, obj_name, default)


def Mapper(keys: Generic[K], items: List[T]) -> Dict[K, T]:
    gen_args = generic_args(keys)
    assert len(gen_args) == len(items)

    return dict(zip(gen_args, items))


# def recursive_import(src: Path, package: str):
#     imported_items = {}
#
#     # Traverse all modules and packages within the directory
#     for module_info in pkgutil.walk_packages([src.parent.__str__()]):
#         module_name = module_info.name
#         print(module_info)
#         if module_name == src.stem: continue
#
#         module = importlib.import_module(f'.{module_name}', package)
#         print(module)
#         # If the module has an __all__, import only those symbols
#         if hasattr(module, '__all__'):
#             for name in module.__all__:
#                 imported_items[name] = getattr(module, name)
#
#     return imported_items
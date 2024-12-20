from KUtils.Typing import *
import inspect

class Argpack:
    def __str__(self):
        out = self.args.__str__() + '\n' + self.kwargs.__str__()
        return out

    def __init__(self, *args, **kwargs):
        self.args = args or []
        self.kwargs = kwargs or {}

    def add(self, value: Any, keyword: str =None):
        if None is keyword:
            self.args.append(value)
        else:
            self.kwargs[keyword]=value

    def call(self, fun: Callable[..., T]) -> T:
        return fun(*self.args, **self.kwargs)

def argkeys(f: object)->List[str]:
    spec = inspect.getfullargspec(f)
    signature = inspect.signature(f).parameters
    sig_keys = list(signature.keys())
    return list(set(spec.args + spec.kwonlyargs + sig_keys))
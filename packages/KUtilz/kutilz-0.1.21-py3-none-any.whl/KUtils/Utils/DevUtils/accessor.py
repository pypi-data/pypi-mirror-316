import functools
from KUtils.Typing import *
from KUtils.Utils.DevUtils.BasePropertyWrapper import BaseProperptyWrapper

class accessor(BaseProperptyWrapper):
    @classmethod
    def ondict(cls,
               target: str
               ) -> Callable[[Any], T]:
        return functools.partial(cls, target=target)

    def __init__(self,
                 initializer: Callable[[Any], T],
                 target: str,
                 key: str = None,
                 default: T = None):

        key = key or initializer.__name__

        fset = lambda slf, item: (getattr(slf, target).__setitem__(key, item))
        fdel = lambda slf: getattr(slf, target).__delitem__(key)
        fget = lambda slf: getattr(slf, target).get(key, default)
        super().__init__(fget, fset, fdel)


if __name__ == '__main__':
    class Dumpy:
        @accessor.ondict('dummy')
        def fucker(self) -> str: ...

        def __init__(self):
            self.dummy = {}


    dd = Dumpy()
    dd.fucker = 'shit'
    print(dd.fucker)

    print(dd.dummy)
    del dd.fucker
    print(dd.dummy)
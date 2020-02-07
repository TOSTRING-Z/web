import numpy as np
import pandas as pd
class test(object):
    def __init__(self,id):
        self.id = id
    def __new__(cls,*args):
        if not hasattr(cls,'_inst'):
            cls._inst = super(test,cls).__new__(cls)
        return cls._inst
    def __repr__(self):
        return 'print => ' + str(self.id)
if __name__ == '__main__':
    import sys
    from typing import Any, Callable, Generic, Dict, Iterable, Mapping, Optional, Sequence, Tuple, Type, TypeVar, NamedTuple, Union, overload
    _T = TypeVar("_T")
    print(_T)

    ts = test(2)
    print(ts.id)
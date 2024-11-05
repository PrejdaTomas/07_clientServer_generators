import typing
import types
import multiprocessing, threading
import json
import re
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt, pow
from time import sleep

class Constants(object):
    run: bool = True
    verbose: bool = True
    
    _refCount: int = 0
        
    @classmethod
    def __new__(cls, *args, **kwargs) -> typing.Self:
        if cls._refCount == 0:
            print(f"Instantiating {cls.__name__}!")
            nuObject= super(Constants, cls).__new__(cls)
            cls._refCount += 1
            return nuObject
        
        print(f"{cls}: cannot instantiate a new entity in the singleton pattern")
        

    def __repr__(self) -> str: return (f"<{self.__class__.__name__} singleton @ <{hex(id(self))}>")
    def __del__(self) -> None: print(f"Terminating the {self}!\n")
    
constants = Constants()
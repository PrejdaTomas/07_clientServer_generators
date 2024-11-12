from BaseClasses import Singleton, Instantiable
import typing
import types
import threading
import re

from time import sleep
from math import sin, cos


class Constants(Singleton):
    run: bool = True
    _verbose: bool = True
    runServerLoop: bool = True
    runServerDictTmpKey: str = "tmp_serverStartupAssignment"
    _refCount: int = 0
    
constants = Constants()
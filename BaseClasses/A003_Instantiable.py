from .A002_Picklable import Picklable

class Instantiable(Picklable):
    _instantiable: bool = True
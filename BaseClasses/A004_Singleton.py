from .A000_BaseMeta import Self, Type
from .A003_Instantiable import Instantiable

class Singleton(Instantiable):
    def __new__(cls, *args, **kwargs) -> Self:

        if cls._instancesActive == 0:
            nuInstance = super(Singleton, cls).__new__(cls)
            return nuInstance
        
        raise TypeError(f"{cls.__name__} is a singleton, cannot instantiate more than one instance.")

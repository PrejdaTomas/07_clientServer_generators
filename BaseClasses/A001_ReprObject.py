from typing import Self, Type
from .A000_BaseMeta import BaseMeta

class ReprObject(object, metaclass= BaseMeta):
    def __new__(cls) -> Self:
        nuInstance: Self = super(ReprObject, cls).__new__(cls)
        return nuInstance
        
    def __repr__(self)-> str:
        return f"{self.__class__.__name__} <{hex(id(self))}>"
    
    def __del__(self) -> str:
        self.__class__._instancesActive -= 1
        return f"{self} TERMINATED!"



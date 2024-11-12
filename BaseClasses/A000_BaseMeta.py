from typing import Any, Self, Type, Dict

class BaseMeta(type):
    _verbose:           bool = False
    _instantiable:      bool = False
    _instanceCounter:   int 
    _instancesActive:   int 
    
    def __new__(cls, classname: str, bases: str, attributes: Dict[str, any]) -> Type:
        print(f"Creating a new class: {classname}")
        nuClass: Type = super(BaseMeta, cls).__new__(cls, classname, bases, attributes)
        attributes.get("_instantiable", False)
        nuClass._instanceCounter = 0
        nuClass._instancesActive = 0
        nuClass._verbose         = False
        
        return nuClass
        
    def __call__(cls, *args, **kwargs) -> Self|None:
        if cls._instantiable:
            print(f"Instantiating a new {cls.__name__} instance")
            for arg in args:(f"\t- sending in {arg}: {type(arg)}")
            for kw in kwargs:(f"\t- sending in {kw}: {kwargs[kw]}: {type(kwargs[kw])}")
            nuInstance: Self = super(BaseMeta, cls).__call__(*args, **kwargs)
            nuInstance.__class__._instancesActive += 1    #ja tady zvedal counter pro instanci, ne pro class
            nuInstance.__class__._instanceCounter += 1    #ja tady zvedal counter pro instanci, ne pro class
            print(f"BaseMeta.__call__: finished instantiating a {cls}, number={nuInstance._instanceCounter}, active={nuInstance._instancesActive}")
            return nuInstance
        
        else:
            print(f"Cannot instantiate a new {cls.__name__} instance, returning None")
            return None
    
    def __repr__(cls) -> str:
        return f"{cls.__name__}"
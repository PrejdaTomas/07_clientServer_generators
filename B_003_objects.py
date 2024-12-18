from __future__ import annotations
from B_000_globalDependecies import typing, types, threading, sin, cos, sqrt, sleep
import B_001_decorators
from B_002_helperFuncs import divBy2, NoneOrBool



class reprObject(object):
    def __repr__(self)-> str: return f"{self.__class__.__name__} <{hex(id(self))}>"



class RandomPositionWrapper(reprObject):
    def __init__(self) -> None:
        self.r = 0.5
        self.x = 0.0
        self.y = self.r
        self.t = 0.0
        self.thread = self.start()
        
        
    def start(self) -> None:
        thread = threading.Thread(
            target=self.update,
            name=f"{self}__RUN"
        )
        thread.start()
        return thread
        
    def update(self) -> None:
        while True:
            self.x = self.r*cos(self.t)
            self.y = self.r*sin(self.t)
            self.t += 0.05
            self.r += 0.025
            sleep(0.1)
    
    def givePosition(self) -> typing.Tuple[float, float]:
        return (self.x, self.y)
            
        
        
        
class NodeWrapper(reprObject):
    def __init__(self) -> None:
        self._exiting: bool = False
        self.node_gen: typing.Generator[int, typing.Any, None] = self._initialize_node()
        self.send(None)  # Initialize the generator

    @B_001_decorators.info
    def _initialize_node(self) -> typing.Generator[int, typing.Any, None]:
        output = 1
        while not self._exiting:
            acceptedIpt = yield output
            print(f"{self}, {acceptedIpt=}")
            if not (NoneOrBool(acceptedIpt)): 
                raise TypeError(f"You've sent a non-boolean arg {acceptedIpt}: {type(acceptedIpt)}")
            
            if acceptedIpt:  
                output += 1
            else:
                print("nothing!")
                output += 0

    def send(self, value: typing.Any) -> typing.Any:
        return self.node_gen.send(value)

    def close(self) -> None:
        self._exiting = True
        #try: self.node_gen.close()
        #except StopIteration:
        #    print(f"{self}: terminated!")

class HostWrapper(reprObject):
    def __init__(self, node_wrapper: NodeWrapper) -> None:
        self._exiting: bool = False
        self.node_wrapper: NodeWrapper = node_wrapper
        self.host_gen: typing.Generator[int, typing.Any, None] = self._initialize_host()
        self.send(None)  # Initialize the generator

    @B_001_decorators.info
    def _initialize_host(self) -> typing.Generator[int, typing.Any, None]:
        while not self._exiting:
            sent_value = yield self.node_wrapper.node_gen.send(None)
            print(f"host <{self}>: SENDING {sent_value}: {type(sent_value)}")
            nodeResponse = self.node_wrapper.send(sent_value)
            print(f"\tCurrent node object: {self.node_wrapper.node_gen}")
            print(f"\tThe node response is: {nodeResponse}")

            if divBy2(nodeResponse): 
                print(f"\t\thost <{self}>: ACTION!")
            else: 
                print(f"\t\thost <{self}>: NOTHING!")

    def close(self) -> None:
        self._exiting = True
        #try: self.host_gen.send(None)
        #except StopIteration:
        #    print(f"{self}: terminated!")

    def send(self, value: typing.Any) -> typing.Any:
        return self.host_gen.send(value)

class HostWrapperTarget(HostWrapper):
    @B_001_decorators.info
    def _initialize_host(self) -> typing.Generator[int, typing.Any, None]:
        while not self._exiting:
            sent_value = yield self.node_wrapper.node_gen.send(None)
            print(f"host <{self}>: SENDING {sent_value}: {type(sent_value)}")
            nodeResponse = self.node_wrapper.send(sent_value)
            print(f"\tCurrent node object: {self.node_wrapper.node_gen}")
            print(f"\tThe node response is: {nodeResponse}")

class NodeWrapperTarget(NodeWrapper):
    def __init__(self, target: object) -> types.NoneType:
        self._exiting: bool = False
        self.node_gen: typing.Generator[int, typing.Any, None] = self._initialize_node(target)
        self.send(None)  # Initialize the generator


    @B_001_decorators.info
    def _initialize_node(self, target: RandomPositionWrapper) -> typing.Generator[int, typing.Any, None]:
        while not self._exiting:
            acceptedIpt = yield target.givePosition()
            
            if acceptedIpt == "stop":
                print(f"{self}: koncim!")
                self.close()

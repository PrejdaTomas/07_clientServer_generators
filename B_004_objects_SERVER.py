from __future__ import annotations
import http.client
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import BaseRequestHandler

from B_000_globalDependecies import typing, sleep,threading, constants
from B_002_helperFuncs import convertString
from http.server import HTTPServer, BaseHTTPRequestHandler

from BaseClasses import Singleton

#ip adresa =  193.84.167.78
#python -m http.server <port> --bind 193.84.167.78
# 193.84.167.78:<port>

class HTMLhandler(object):
    
    @staticmethod
    def _encode(iptStr: str, encoding: typing.Optional[str] = "utf-8") -> bytes:
        return bytes(iptStr, encoding)
    
    @staticmethod
    def _h1Wrapper(iptStr:str) -> str:
        var="h1"
        return f"<{var}>{iptStr}</{var}>"
    
    @staticmethod
    def _bodyWrapper(iptStr:str) -> str:
        var="body"
        return f"<{var}>{iptStr}</{var}>"

    @staticmethod
    def _htmlWrapper(iptStr:str )-> str:
        var="html"
        return f"<{var}>{iptStr}</{var}>"
    
    @staticmethod
    def _header(iptStr:str) -> str:
        return HTMLhandler._htmlWrapper(HTMLhandler._bodyWrapper(HTMLhandler._h1Wrapper(iptStr)))


    def header(iptStr:str) -> bytes:
        return HTMLhandler._encode(HTMLhandler._header(iptStr))
    


class CustomHTTPServer_RequestReceiver(Singleton, HTTPServer):
    userInputs: typing.Dict[CustomHTTPServer_Server, typing.List[typing.Any]]           = {}
    results:    typing.DefaultDict[CustomHTTPServer_Server, typing.List[typing.Any]]    = {}

    def __new__(cls, *args, **kwargs) -> typing.Self:
        return super(CustomHTTPServer_RequestReceiver, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self,
                 server_address: tuple[str | bytes | bytearray, int],
                 RequestHandlerClass: typing.Callable[[typing.Any, typing.Any, typing.Self], BaseRequestHandler],
                 bind_and_activate: bool = False,
                 running: bool = True,
                 masterObject: CustomHTTPServer_Server = None
                ) -> None:
        
        super(CustomHTTPServer_RequestReceiver, self).__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.master:CustomHTTPServer_Server = masterObject
        self.keepRunning:bool               = running
        self.keepCalculating:bool           = True
        self.calculationThread:None|threading.Thread = None
        try:
            self.__class__.userInputs[self.master]  is not None
            self.__class__.results[self.master]     is not None
        except:
            self.__class__.userInputs[self.master]  = []
            self.__class__.results[self.master]     = []
    
    def serve_forever(self, poll_interval: float = 0.5) -> None:
        print("-----------------------------------------RECEIVER.SERVE_FOREVER")
        while self.keepRunning:
            self.handle_request()
            print(self.__class__.userInputs)
        print("server is shutting down")
        
    def loopCalculation(self):
        from B_000_globalDependecies import sin
        t= 0.0
        while self.keepCalculating: 
            self.results[self.master].append(sin(t))
            t += 0.05
            sleep(0.10)
    
    def loopCalculationThreadMaker(self) -> threading.Thread:
        self.keepCalculating = True
        nuThread = threading.Thread(target= self.loopCalculation, args=())
        nuThread.daemon = True
        nuThread.start
        return nuThread
        
    
    
            
       
class CustomHTTPServer_RequestProcessor(BaseHTTPRequestHandler):
    """
    CustomHTTPServer_RequestProcessor je docasny objekt, ktery vznikne pri zpracovavani prijateho requestu z CustomHTTPServer_RequestReceiver.
    Neni mozne na nem nechat cokoliv bezet asynchronne, atp, pro kazde zpracovani prijateho requestu se vytvori nova instance tohoto objektu.
    Veskere persistentni operace musi bezet bud na CustomHTTPServer_RequestProcessor.server, coz je instance CustomHTTPServer_RequestReceiver,
    nebo primo na obalovacim objektu CustomHTTPServer_Server
    """
    callsPOST:  int = 0
    callsGET:   int = 0
    processorsToOutputs: typing.Dict[typing.Self, float] = {}
    processorsToOutputs: typing.Dict[typing.Self, float] = {}
    serversToProcessors: typing.Dict[CustomHTTPServer_Server, typing.Self] = {} 
    
    def _responseWithHeaders(self, header: str = "Content-type", dataType: str = "text/plain") -> None:
        self.send_response(200)
        self.send_header(keyword=header, value=dataType)
        self.end_headers()
        
    def do_GET(self) -> None:
        print("-----------------------------------------PROCESSOR.GET")
        self.__class__.callsGET += 1 
        self._responseWithHeaders(header="Content-type", dataType="text/plain")
        self.wfile.write(f"GET__PROCESSOR: {self}".encode("utf-8"))

    
    def do_POST(self) -> None:
        print("-----------------------------------------PROCESSOR.POST")
        self.__class__.callsPOST += 1
        contentByteLength   = int(self.headers['Content-Length'])
        postReceivedData    = self.rfile.read(contentByteLength).decode('utf-8')
        
        postReceivedDataHandled = convertString(postReceivedData)
        if postReceivedDataHandled == False:
            print(f"{self} shutting {self.server} down!")
            self.server.keepRunning = False
        
        elif postReceivedData == "stopLoop":
            print(f"{self} shutting {self.server.loopCalculation} down!")
            self.server.keepCalculating = False
            self.server.calculationThread = None
        
        elif postReceivedData == "startLoop":
            print(f"{self} starting {self.server.loopCalculation}!")
            self.server.calculationThread = self.server.loopCalculationThreadMaker()
              
        self.server.__class__.userInputs[self.server.master].append(postReceivedDataHandled)
        #vypada to krkolomne, ale ... pristupuji k tridnimu atributu userInputs a keyem je encapsulator celeho procesu.

        self._responseWithHeaders(header="Content-type", dataType="text/plain")
        self.wfile.write(f"SET__PROCESSOR: {self}\n".encode("utf-8"))
        self.wfile.write(f"SET__RECEIVER: {self.server}\n".encode("utf-8"))
        self.wfile.write(f"SET__MASTER: {self.server.master}\n".encode("utf-8"))
        self.wfile.write(f"SET__USERINPUTS: {self.server.__class__.userInputs}".encode("utf-8"))
        self.wfile.write(f"SET__RESULTS: {self.server.__class__.results}".encode("utf-8"))
    

class CustomHTTPServer_Server(Singleton):
    ip: str
    port: int
    
    def __new__(cls, *args, **kwargs) -> CustomHTTPServer_Server:
        return super(CustomHTTPServer_Server, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, ip: str, port: int) -> None:
        self.ip             = ip
        self.port           = port
        self.receiver       = CustomHTTPServer_RequestReceiver(server_address=(self.ip, self.port),
                                                               RequestHandlerClass=CustomHTTPServer_RequestProcessor,
                                                               masterObject=self,
                                                               bind_and_activate=False,
                                                               running=True)

         
    def start(self) -> threading.Thread:
        self.receiver.keepRunning   = True
        runThread                   = threading.Thread(target=self.receiver.serve_forever,args=())
        runThread.daemon            = False #daemon True se ujisti, ze thread skonci a python program dojede do konce.
        runThread.start()
        return runThread
    
    def stop(self) -> None:
        self.receiver.keepRunning = False
    
    def __str__(self) -> str:
        strTop:str = f"|   {self.__class__.__name__} @ {hex(id(self))}"
        strMid:str = f"|   ip: {self.ip}"
        strBot:str = f"|   port: {self.port}"
        maxSymbols: int = max(len(strTop), len(strMid), len(strBot))
        _:str = (8+maxSymbols)*"-"
        bracket: str = f"[{_}]"
        
        strTop += (" "*(len(bracket) - 1 - len(strTop)) + "|") 
        strMid += (" "*(len(bracket) - 1 - len(strMid)) + "|") 
        strBot += (" "*(len(bracket) - 1 - len(strBot)) + "|") 
        
        returnVal: str = "\n".join(("",bracket, strTop, strMid, strBot, bracket,""))
        return returnVal
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} @ {hex(id(self))}>"
      
    def __del__(self) -> None:
        #self.stop()
        #self.receiver.server_close()
        print(f"Terminating {self.__repr__()}")
        
     
    

    #server.stop()   


a=CustomHTTPServer_Server("5", 5)


#curl -X GET http://193.84.167.78:8080 & echo "\n" &curl -X POST http://193.84.167.78:8080 -H "Content-Type: text/plain" -d "false"


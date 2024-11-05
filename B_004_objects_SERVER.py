from B_000_globalDependecies import typing,json,sleep,threading
from B_002_helperFuncs import jsonQuotes
import B_003_objects_BKGROUND
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import http.client

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
    


from http.server import HTTPServer, BaseHTTPRequestHandler
class CustomServer(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        htmlStr: str = HTMLhandler.header("HELLO WORLD!")
        self.wfile.write(htmlStr)
    
    def do_POST(self) -> None:
        print("do_Post!")
        content_length  = int(self.headers['Content-Length'])
        post_data       = jsonQuotes(self.rfile.read(content_length)[1:-1].decode("utf-8"))
        #pozor: json nemá rád mezery za dvoutečkou, začne to uvozovkami jednoduchymi, dvojte uvozovky nenacte - musim si jevyrobit z jednoduchych
        print(f"Received POST data: {post_data}, {type(post_data)}")
        
        data            = json.loads(s=post_data)
        name        = data.get("name", "World")
        
        response    = json.dumps({"message":f"Hello,{name}!" }).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response)
        
class CustomServerHandler:
    def __init__(self, ip: str= None, port: int= None) -> None:
        self._ip: str = ip
        self._port: int = port
        self._server = self.startServer()
    
    
    def startServer(self) -> HTTPServer:
        print(f"{self} started!")
        myServer = HTTPServer(server_address=(self._ip, self._port), RequestHandlerClass=CustomServer)
        myServer.serve_forever()
        return myServer
    
    def stopServer(self) -> None:
        self.server.server_close()
        print(f"{self} stopped!")
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:: {self._ip}:{self._port} @ <{hex(id(self))}>>"
    

class CustomServerClientNode(BaseHTTPRequestHandler):
    runningServers: typing.Dict[str, typing.Self] = {}
    runningResults: typing.Dict[typing.Self, float] = {}
    runningHandlers: typing.Dict["CustomServerHandlerClientNode", typing.Self] = {}
    calls: int = 0
    #DOES NOTHING
    #def __init__(self, *args, directory=None, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    print("init!")
    #    self.__class__.runningHandlers[0] = self        
    
    def do_GET(self) -> None:
        print("GET DOING!")
        #zkousim handler strcit do dictu...
        if self.__class__.calls ==0:
            self.__class__.runningHandlers[0] = self
            
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        htmlStr: str = HTMLhandler.header("Client-Node test")
        self.wfile.write(htmlStr)
        self.__class__.calls += 1
    
    def do_POST(self) -> None:
        content_length  = int(self.headers['Content-Length'])
        print(self, self.__class__.runningResults)
        post_data       = str(self.__class__.runningResults[self])
        
        
        response    = "ahoj!"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(post_data)

    #takto jsem obešel neschopnost přistoupit k self
    def run_loop(self):
        i = 0
        target=self
        while True:
            print(target)
            CustomServerClientNode.runningResults[target] = i
            print(CustomServerClientNode.runningResults)
            print("Running background task...")
            sleep(10)  # Simulate a task that runs every 5 seconds
            i+=1

class CustomServerHandlerClientNode:
    def __init__(self, ip: str= None, port: int= None) -> None:
        self._ip:       str = ip
        self._port:     int = port
        self._server        = self.startServer()
    
    
    def startServer(self) -> HTTPServer:
        print(f"{self} started!")
        myServer = HTTPServer(server_address=(self._ip, self._port), RequestHandlerClass=CustomServerClientNode)
        #snazim se dostat do dictu handleru jeho instanci

        conn = http.client.HTTPConnection(self._ip, self._port)
        conn.request("GET", "/")

        #tady to mrzne
        response = conn.getresponse()
        #nefunguje
        print(myServer.RequestHandlerClass.runningHandlers)
        myServer.RequestHandlerClass.runningHandlers[myServer] = myServer.RequestHandlerClass.runningHandlers[0]
        myServer.RequestHandlerClass.runningHandlers[0] = None
        print(myServer.RequestHandlerClass.runnigHandlers)
        print(myServer)
        #loop_thread = threading.Thread(
        #    target=myServer.RequestHandlerClass.run_loop,
        #    args=(myServer.RequestHandlerClass.runningServers[myServer.server_address],)
        #)
        loop_thread = threading.Thread(
                    target=myServer.run_loop)
        loop_thread.daemon = True  # This allows the thread to exit when the main program does
        loop_thread.start()

        
        
        myServer.serve_forever()
        return myServer
    
    def stopServer(self) -> None:
        self.server.server_close()
        print(f"{self} stopped!")
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:: {self._ip}:{self._port} @ <{hex(id(self))}>>"
    
    
    
if __name__ == "__main__":
    server = CustomServerHandlerClientNode(ip='193.84.167.78', port=8080)
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()

#curl -X POST http://193.84.167.78:8080 -H "Content-Type: application/json" -d '{"name":"Alice","surname":"Pfeifer"}'     
        
"""
application/json:
Used for JSON data. Commonly used in REST APIs.
Example: {"name": "Alice"}
application/xml:
Used for XML data.
Example: <name>Alice</name>
text/html:
Used for HTML documents.
Example: <html><body>Hello, World!</body></html>
text/plain:
Used for plain text data.
Example: Hello, World!
application/x-www-form-urlencoded:
Used for form submissions. Data is encoded as key-value pairs.
Example: name=Alice&age=30
multipart/form-data:
Used for forms that include file uploads. It allows for sending files and data together.
Example: Used in file upload forms.
application/octet-stream:
Used for binary data. This is a generic type for binary files.
Example: Used when the type is unknown.
image/jpeg:
Used for JPEG images.
Example: Sending image files.
image/png:
Used for PNG images.
audio/mpeg:
Used for MPEG audio files.
"""
from B_000_globalDependecies import constants
from B_002_helperFuncs import convertString
import B_003_objects_BKGROUND
from B_004_objects_SERVER import CustomServerHandler

#ip adresa =  193.84.167.78
#python -m http.server <port> --bind 193.84.167.78
# 193.84.167.78:<port>


if  __name__    ==      "__main__":
    node_wrapper = B_003_objects_BKGROUND.NodeWrapperTarget(B_003_objects_BKGROUND.RandomPositionWrapper())
    host_wrapper = B_003_objects_BKGROUND.HostWrapperTarget(node_wrapper)
    
    server = CustomServerHandler(ip='193.84.167.78', port=8080)
    while constants.run:
        value           = input("user input: ")
        sendVal         = convertString(value)
        retVal          = [[*host_wrapper.send(sendVal)]] #vraci tuple, potrebuji list v listu
        constants.run   = False if (sendVal == False or sendVal == "stop") else True

        

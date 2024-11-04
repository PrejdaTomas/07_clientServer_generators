from B_000_globalDependecies import plt
from B_002_helperFuncs import convertString
import B_003_objects as B_003_objects


if __name__ == "__main__":
    lojzek = B_003_objects.RandomPositionWrapper()
    
    plt.ion() #interactive on
    figure = plt.figure()
    ax = figure.add_subplot()
    ax.grid()
    scatter = ax.scatter([0], [0])
    ax.set_xlim((-5, 5))
    ax.set_ylim((-5, 5))
    plt.show()
    
    
    if True:
        node_wrapper = B_003_objects.NodeWrapperTarget(lojzek)
        host_wrapper = B_003_objects.HostWrapperTarget(node_wrapper)
        
        while True:
            value       = input("What ")
            sendVal     = convertString(value)
            retVal      = [[*host_wrapper.send(sendVal)]] #vraci tuple, potrebuji list v listu
            actualData  = scatter.get_offsets().tolist()
            scatter.set_offsets(actualData + retVal)

            figure.canvas.draw()
            plt.pause(0.01)
        
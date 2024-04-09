import sys
sys.path.insert(0, "..")
from opcua import ua
from opcua import Client
from cin import Cin
from utils import setValueCheck
from factory import *




if __name__ == "__main__":
    client = Client("opc.tcp://127.0.0.1:4840")
    machine1 = Machine(client, M1, 1, 1)
    machine2 = Machine(client, M2, 2, 1)
    machine3 = Machine(client, M1, 3, 1)
    machine4 = Machine(client, M2, 4, 1)
    machine5 = Machine(client, M1, 5, 1)
    machine6 = Machine(client, M2, 6, 1)
    machine7 = Machine(client, M3, 7, 1)
    machine8 = Machine(client, M4, 8, 1)
    machine9 = Machine(client, M3, 9, 1)
    machine10 = Machine(client, M4, 10, 1)
    machine11 = Machine(client, M3, 11, 1)
    machine12 = Machine(client, M4, 12, 1)
    
    try:
        client.connect()

        cin1 = Cin(client, 1)
        cin1.get_nodes()
        cin1.receivePieces(2, 1)
        




    except Exception as e:
        print(e)
    finally:
        client.disconnect()
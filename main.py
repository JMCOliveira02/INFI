import sys
sys.path.insert(0, "..")
from opcua import ua
from opcua import Client
from cin import Cin
from utils import setValueCheck
from factory import *
from database import *
from orders import *
from importlib import reload






if __name__ == "__main__":
    client = Client("opc.tcp://127.0.0.1:4840")
    machine_types = [M1, M2, M1, M2, M1, M2, M3, M4, M3, M4, M3, M4]
    machines = [Machine(client, machine_types[i], i+1, 1) for i in range(12)]
    piece_ordered = 3
    transformations = {}

    try:
        client.connect()
        """cin1 = Cin(client, 1)
        cin1.get_nodes()
        cin1.receivePieces(2, 1) """
        db = Database()
        db.connect()
        currOrder=parseOrderCSV(db.get_earliest_order())
        print(f"Current Order: {currOrder.workpiece}")

        for i in range(12):
            transformations[i] = machines[i].findTransformations(currOrder.workpiece)
        
        chosenMachineId, chosenTransformation = chooseTransformation(transformations)

        machines[chosenMachineId - 1].performTransformation(chosenTransformation, 0)

        storePiece(client, 0)





    except Exception as e:
        print(e)
    finally:
        client.disconnect()
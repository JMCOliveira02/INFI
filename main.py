import sys
sys.path.insert(0, "..")
from opcua import ua
from opcua import Client
from cin import Cin
from utils import setValueCheck
from factory import *
from database import *
from orders import *
from scheduling import *
from importlib import reload


# **********Variáveis de configuração**********

# Número de máquinas
numMachines = 12
# Tempo mudança de ferramenta
tool_change_time = 30000 # ms

# Transformações possíveis e respetivos tempos
# edges = [
#     # nó 1, nó 2, ferramenta, tempo
#     ('P1', 'P3', "T1", 45000),
#     ('P4', 'P6', "T2", 25000),
#     ('P2', 'P8', "T1", 45000),
#     ('P3', 'P4', "T2", 15000),
#     ('P3', 'P4', "T3", 25000),
#     ('P4', 'P7', "T3", 15000),
#     ('P4', 'P5', "T4", 25000),
#     ('P8', 'P9', "T5", 45000),
#     ('P8', 'P7', "T6", 15000)
# ]

# *********************************************



# if __name__ == "__main__":
#     client = Client("opc.tcp://127.0.0.1:4840")
#     # Define layout da fábrica
#     machine_types = [M1, M2, M1, M2, M1, M2, M3, M4, M3, M4, M3, M4]
#     # Inicialização das máquinas
#     machines = [Machine(client, machine_types[i], i+1, 1) for i in range(numMachines)]

#     try:
#         # Grafo com todos os caminhos possíveis
#         G = generateGraph(edges)

#         # Encontrar os caminhos possíveis para a peça P6
#         nodes_, edges_ = findTransformations(G, 'P7')
#         print("Nodes:")
#         print(nodes_)
#         print("Edges:")
#         print(edges_)


#         # Conecta cliente OPC-UA
#         client.connect()

#         # # Inicializa base de dados
#         # db = Database()
#         # # Conecta à base de dados
#         # db.connect()
        
#         # """cin1 = Cin(client, 1)
#         # cin1.get_nodes()
#         # cin1.receivePieces(2, 1) """


#         # Lê o primeiro pedido da base de dados
#         # currOrder=parseOrderCSV(db.get_earliest_order())
#         # Imprime o pedido
#         # printOrder(currOrder)
#         #print(f"Current Order: {currOrder.workpiece}")

#         # for i in range(numMachines):
#         #     transformations[i] = machines[i].findTransformations(currOrder.workpiece)

#         # print(transformations)
        
#         #chosenMachineId, chooseTransformation = chooseTransformation(transformations)

#         #machines[chosenMachineId - 1].performTransformation(chooseTransformation, 0)

#         #storePiece(client, 0)



#     except Exception as e:
#         print(e)
#     finally:
#         client.disconnect()


# while True:
        
#     pass
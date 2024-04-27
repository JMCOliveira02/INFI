import sys
sys.path.insert(0, "..")
import modules.shopfloor.gen_cin as gen_cin
from modules.mes.scheduling import *
from modules.communications.plc_communications import *
import traceback
import time



def initialize(show_credits=True):
    
    if credits:
        printAuthorsCredits()
  
    # Inicializa cliente OPC-UA
    client = PLCCommunications(CONSTANTS["opcua_connection"])

    # Conecta ao cliente OPC-UA
    try:
        client.clientConnect()
    except Exception as e:
        if e is NameError.ClientAlreadyConnected:
            print("Error:", e)
            pass
        elif e is NameError.NoConnectionProvided:
            print("Error:", e)
            sys.exit()
        else:
            print(traceback.format_exc())
            sys.exit()


    # Gerar grafo e grafo simples
    G = generateGraph()
    G_simple = generateSimpleGraph()

    # inicialização de classes
    cin = gen_cin.GenCin(client=client)

    return client, G, G_simple, cin

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



if __name__ == "__main__":

    # inicialização
    client, G, G_simple, cin = initialize()

    while True:
        try:
            cin.spawnPieces([1, 1])
            # cin.spawnPieces(1, 3)
            # cin.spawnPieces(2, 3)
            # time.sleep(10)
            #schedule(G_simple, G, client=client, piece='P5')

            # terminar programa
            client.clientDisconnect()
            sys.exit()


        except Exception as e:
            if e is NameError.NoGeneratorsAvailable:
                print("Error:", e)
                pass
            else:
                print(traceback.format_exc())
                client.clientDisconnect()
                sys.exit()


        # try:
        #     schedule(G_simple, G, client=client, piece='P5')
        #     client.clientDisconnect()
        #     sys.exit()
            
        # except Exception as e:
        #     if e is NameError:
        #         print("Error:", e)
        #         pass
        #     else:
        #         print(traceback.format_exc())
        #         client.clientDisconnect()
        #         sys.exit()
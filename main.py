import sys
sys.path.insert(0, "..")
import modules.mes.production_order as production_order
from modules.communications.plc_communications import PLCCommunications
from modules.mes.transformations import generateGrahps
from modules.mes.scheduling import Scheduling
from modules.shopfloor.recipes import Recipe
from modules.shopfloor.gen_cin import GenCin
from utils import *
from database import *
import traceback




def initialize(show_credits=True):
    
    if show_credits:
        printAuthorsCredits()
  
    # Inicializa cliente OPC-UA
    client_connection = CONSTANTS["opcua_connection"]
    client = PLCCommunications(opcua_connection=client_connection)

    # Conecta ao cliente OPC-UA
    try:
        client.clientConnect()
    except Exception as e:
        print(traceback.format_exc())
        sys.exit()

    # Conecta à base de dados
    try:
        db = Database()
        db.connect()
    except Exception as e:
        print(traceback.format_exc())
        sys.exit()


    # Gerar grafo e grafo simples
    G, G_simple = generateGrahps()

    schedule = Scheduling(client)

    # inicialização de classes
    cin = GenCin(client=schedule.client)

    return client, schedule, G, G_simple, cin, db

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

    recipes = [Recipe]*12

    # inicialização
    client, schedule, G, G_simple, cin, db = initialize()

    #po = [3, 5, "2021-06-01"]

    #production_order_ = production_order.ProductionOrder(po)
    #production_order_.printProductionOrder()

    # Atualiza tempo inicial na DB 
    initialTime = db.update_initial_time()
    currTimeSeconds = (datetime.datetime.now() - initialTime).seconds
    day = currTimeSeconds / 60
            
            

    while True:
        currTimeSeconds = (datetime.datetime.now() - initialTime).seconds
        day = currTimeSeconds // 60
        print(currTimeSeconds, day)

        # Simular o tempo de execução de cada loop
        #time.sleep(0.5)
        
        """ try:
            # para cada peça escalorar transformação e atribuir a receita
            production_order_.generateRecipes()   
            client.clientDisconnect()
            sys.exit()

        except Exception as e:
            if e.name == "InvalidNumberPieces":
                print(e.args[0])
                client.clientDisconnect()
                sys.exit()
            else:
                print(traceback.format_exc())
                client.clientDisconnect()
                sys.exit() """


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
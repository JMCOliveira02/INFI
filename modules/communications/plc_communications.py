from opcua import ua, Client
import emoji
import time

from utils import CONSTANTS, bcolors
from modules.mes.production_order import ProductionOrder
from modules.shopfloor.recipes import Recipe




class PLCCommunications:

    def __init__(self, opcua_connection):
        '''
        Inicializa a classe PLCCommunications.

        args:
            opcua_connection: string com o endereço do servidor OPC-UA.
        return:
            None
        '''
        self.opcua_connection = opcua_connection
        self.client = None
        self.time_to_sleep = 0.1



    def clientConnect(self):
        '''
        Função para conectar ao cliente OPC-UA.

        args:
            None
        return:
            None
        '''
        print(f'\n{bcolors.BOLD}[Communications]{bcolors.ENDC} Connecting to OPC-UA server...', end=" ", flush=True)
        self.client = Client(self.opcua_connection)
        self.client.connect()
        print(emoji.emojize('Connected to OPC-UA server! :check_mark_button:'))
        return



    def clientDisconnect(self):
        '''
        Função para desconectar do cliente OPC-UA.

        args:
            None
        return:
            None
        '''
        print(f'\n{bcolors.BOLD}[Communications]{bcolors.ENDC} Disconnecting from OPC-UA server...', end=" ", flush=True)
        self.client.disconnect()
        print(emoji.emojize('Disconnected from OPC-UA server! :check_mark_button:'))



    def getMachineState(self, machine_id):
        '''
        Função para obter o estado de uma máquina.

        args:
            machine_id: id da máquina.
        return:
            state: estado da máquina.
        '''
        time.sleep(self.time_to_sleep) # pequeno compasso de espera para o PLC se atualizar
        machine = self.client.get_node(CONSTANTS["MachineState"]["NamespaceIndex"] + "[" + str(machine_id) + "]")
        return machine.get_value()
    


    def getCurrentTool(self, machine_id):
        '''
        Função para obter a ferramenta atual de uma máquina.

        args:
            machine_id: id da máquina.
        return:
            tool: ferramenta atual da máquina.
        '''
        time.sleep(self.time_to_sleep) # pequeno compasso de espera para o PLC se atualizar
        tool = self.client.get_node(CONSTANTS["MachineTool"]["NamespaceIndex"] + "[" + str(machine_id) + "]")
        return tool.get_value()
    


    def getPieceTopWH(self, type: int):
        '''
        Função para obter a peça no armazém superior de uma máquina.

        args:
            type (int): tipo da peça.
        return:
            piece: número de peças no armazém superior da máquina.
        '''
        num_pieces = self.client.get_node(CONSTANTS["AvailableTopWh"]["NamespaceIndex"] + "[" + str(type) + "]")
        return num_pieces.get_value()
    


    def setValueCheck(self, node, value, variant_type):
        '''
        Função para enviar um valor em um nó e verificar se 
        o valor foi enviar corretamente.
        
        args:
            node: nó opc-ua.
            value: valor a ser enviado.
            variant_type: tipo do valor.

        return:
            None
        '''
        node.set_value(ua.Variant(value, variant_type))
        while node.get_value() != value:
            pass



    def incomingPiece(self, generator_id: int, num_pieces: int):
        '''
        Função para receber peças no PLC.

        args:
            generator_id (int): id do gerador.
            num_pieces (int): número de peças.
        return:
            None
        '''
        pieces_node = self.client.get_node(CONSTANTS["GenCin"]["NamespaceIndex"] + "[" + str(generator_id) + "]" + CONSTANTS["GenCin"]["Pieces"])
        finish_node = self.client.get_node(CONSTANTS["GenCin"]["NamespaceIndex"] + "[" + str(generator_id) + "]" + CONSTANTS["GenCin"]["Finish"])
        self.setValueCheck(pieces_node, num_pieces, ua.VariantType.Int16)

        while finish_node.get_value() == False:
            pass
        self.setValueCheck(pieces_node, 0, ua.VariantType.Int16) # reset ao número de peças
        return
    


    def sendRecipe(self, recipe: Recipe):
        '''
        Função para enviar uma receita para o PLC.

        args:
            recipe (Recipe): receita a ser enviada.
        return:
            None
        '''
        machine_id_node = self.client.get_node(CONSTANTS["Recipes"]["NamespaceIndex"] + "[" + str(recipe.recipe_id) + "]" + CONSTANTS["Recipes"]["MachineId"])
        piece_in_node = self.client.get_node(CONSTANTS["Recipes"]["NamespaceIndex"] + "[" + str(recipe.recipe_id) + "]" + CONSTANTS["Recipes"]["PieceIn"])
        tool_node = self.client.get_node(CONSTANTS["Recipes"]["NamespaceIndex"] + "[" + str(recipe.recipe_id) +"]" + CONSTANTS["Recipes"]["Tool"])
        time_node = self.client.get_node(CONSTANTS["Recipes"]["NamespaceIndex"] + "[" + str(recipe.recipe_id) + "]" + CONSTANTS["Recipes"]["Time"])
        end_node = self.client.get_node(CONSTANTS["Recipes"]["NamespaceIndex"] + "[" + str(recipe.recipe_id) + "]" + CONSTANTS["Recipes"]["End"])

        time.sleep(self.time_to_sleep) # pequeno compasso de espera para o PLC se atualizar
        self.setValueCheck(machine_id_node, recipe.machine_id, ua.VariantType.Int16)
        self.setValueCheck(piece_in_node, recipe.piece_in, ua.VariantType.Int16)
        self.setValueCheck(tool_node, recipe.tool, ua.VariantType.Int16)
        self.setValueCheck(time_node, recipe.time, ua.VariantType.UInt32)
        self.setValueCheck(end_node, recipe.end, ua.VariantType.Boolean)
        return
    


    def getRecipeState(self, recipe: Recipe):
        '''
        Função para obter o estado de uma receita.

        args:
            recipe (Recipe): receita.
        return:
            recipe (Recipe): receita atualizada.
        '''
        end_node = self.client.get_node(CONSTANTS["Recipes"]["NamespaceIndex"] + "[" + str(recipe.recipe_id) + "]" + CONSTANTS["Recipes"]["End"])
        recipe.end = end_node.get_value()
        return
    


    def sendDelivery(self, order: ProductionOrder):
        '''
        Função para enviar uma entrega para o PLC.

        args:
            order (ProductionOrder): id da ordem.
        return:
            None
        '''
        piece_type_node = self.client.get_node(CONSTANTS["Delivery"]["NamespaceIndex"] + CONSTANTS["Delivery"]["PieceType"])
        quantity_node = self.client.get_node(CONSTANTS["Delivery"]["NamespaceIndex"] + CONSTANTS["Delivery"]["Quantity"])
        send_node = self.client.get_node(CONSTANTS["Delivery"]["NamespaceIndex"] + CONSTANTS["Delivery"]["Send"])

        time.sleep(self.time_to_sleep) # pequeno compasso de espera para o PLC se atualizar
        self.setValueCheck(piece_type_node, order.target_piece, ua.VariantType.Int16)
        self.setValueCheck(quantity_node, order.quantity, ua.VariantType.Int16)
        self.setValueCheck(send_node, True, ua.VariantType.Boolean)
        return



    def getDeliveryState(self, order: ProductionOrder):
        '''
        Função para obter o estado de uma entrega. Se a entrega foi enviada
        procede a alterar o estado da order para DONE.

        args:
            order (ProductionOrder): id da ordem.
        return:
            True: se a entrega foi enviada.
            False: se a entrega não foi enviada.
        '''
        time.sleep(self.time_to_sleep) # pequeno compasso de espera para o PLC se atualizar
        delivery_state = self.client.get_node(CONSTANTS["Delivery"]["NamespaceIndex"] + CONSTANTS["Delivery"]["Send"])
        if delivery_state.get_value() == False:
            order.status = order.DONE
            return True
        return False
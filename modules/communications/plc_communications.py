from opcua import ua, Client
from utils import *
import emoji



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



    def clientConnect(self):
        '''
        Função para conectar ao cliente OPC-UA.

        args:
            None
        return:
            Exception ClientAlreadyConnected: caso o cliente já esteja conectado.
            Exception NoConnectionProvided: não haja link para conexão OPC-UA.
        '''
        if self.client is not None:
            raise NameError("Client OPC-UA already connected!", name="ClientAlreadyConnected")
        elif self.opcua_connection is None:
            raise NameError("No OPC-UA connection provided!", name="NoConnectionProvided")
        
        print(emoji.emojize('Connecting to OPC-UA server... '))
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
        print('Disconnecting from OPC-UA server...')
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
    


    def setValueCheck(self, node: Client, value, variant_type):
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
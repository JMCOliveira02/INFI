from modules.communications.plc_communications import PLCCommunications
from modules.mes.transformations import *




# Estado atual das 12 máquinas (0: livre mas não opera, 1: opera, 2: ocupada, 3: em manutenção)
#cur_machine_state = [None]*12
cur_machine_state = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
    12: None
}

# Ferramenta atual das 12 máquinas
#cur_machine_tool = [None]*12
cur_machine_tool = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
    12: None
}

# Número de peças para caa tipo disponíveis no armazém superior
cur_pieces_top_wh = {
    "P1": None,
    "P2": None,
    "P3": None,
    "P4": None,
    "P5": None,
    "P6": None,
    "P7": None,
    "P8": None,
    "P9": None
}



def updateMachinesState(client_opcua: PLCCommunications):
    '''
    Função para atualizar o estado das máquinas.
    Args:
        client (PLCCommunication): objecto cliente OPC-UA

    Return:
        None
    '''
    for i, state in enumerate(cur_machine_state):
        cur_machine_state[state] = client_opcua.getMachineState(i+1) # No PLC as máquinas não têm ID 0, mas sim de 1 a 12



def updateMachineTool(client_opcua: PLCCommunications):
    '''
    Função para verificar a ferramenta atual da máquina.
    Args:
        client (PLCCommunication): objecto cliente OPC-UA

    Return:
        None
    '''
    for i, tool in enumerate(cur_machine_tool):
        cur_machine_tool[tool] = client_opcua.getCurrentTool(i+1) # No PLC as máquinas não têm ID 0, mas sim de 1 a 12



def updatePiecesTopWh(client_opcua: PLCCommunications):
    '''
    Função para verificar a existência de peças no armazém superior.
    Args:
        client (PLCCommunication): objecto cliente OPC-UA

    Return:
        None
    '''
    for i, piece in enumerate(cur_pieces_top_wh):
        cur_pieces_top_wh[piece] = client_opcua.getPieceTopWH(i+1) # As peças não têm tipo 0, mas sim de 1 a 9



class Scheduling():
    def __init__(self, opcua_client: PLCCommunications):
        self.client = opcua_client



    def __calculateEdgesWeights(self, G):
        '''
        Função para calcular o peso de todas as arestas com base no tempo de transformação, 
        tempo de mudança de ferramenta (se necessário), tempo de manutenção (se necessário),
        se a respetiva máquina está a operar e prioridade de transformação das máquinas de id par.
        Args:
            G (nx.MultiDiGraph): grafo da fábrica

        Return:
            None
        '''
        # atualizar estado das máquinas
        updateMachinesState()
        # atualizar ferramenta das máquinas
        updateMachineTool()

        # cálculo do peso para cada edge
        for edge in G.edges(data=True, keys=True):
            edge_time, tool_time, main_time, machine_time, previous_machine_time = 0, 0, 0, 0, 0
            # tempo de transformação
            edge_time = edge[3]['time']
            # tempo de mudança de ferramenta
            if cur_machine_tool[edge[3]['machine_id']] != edge[3]['tool']: # No PLC as máquinas não têm ID 0, mas sim de 1 a 12
                tool_time = Ttool
            else:
                tool_time = 0
            # tempo de manutenção (verificar estado da máquina)
            if cur_machine_state[edge[3]['machine_id']] == 3:
                main_time = Tmain
            else:
                main_time = 0
            # tempo de máquina atual (verificar se máquina está a operar)
            if cur_machine_state[edge[3]['machine_id']] == 1:
                machine_time = Tmachine
        
            # tempo de máquina anterior (verificar se máquina anterior, de índice impar está ocupada)
            '''
            !!!!!!!!!PODE SER NECESSÁRIO OLHAR PARA AS RECEITAS E NÃO PARA O ESTADO ATUAL DA MÁQUINA
            '''
            if edge[3]['machine_id'] % 2 == 0: # máquina de índice par
                if cur_machine_state[edge[3]['machine_id'] - 1] == 0: # máquina anterior (índice ímpar) não está a produzir
                    previous_machine_time = Tprevious_free
                else:
                    previous_machine_time = Tprevious_busy
            
            # cálculo do peso
            edge_weight = edge_time + tool_time + main_time + machine_time + previous_machine_time
            G[edge[0]][edge[1]][edge[0]+edge[1]+"M"+str(edge[3]["machine_id"])]['weight'] = edge_weight

        return

         


    def __verifyPreviousMachine(self, edge):
        '''
        Função para verificar se a máquina anterior está ocupada.
        Args:
            edge (tuple): aresta do grafo a verificar a máquina anterior

        Return:
            Transformations.Tmain: Máquina anterior está ocupada. 0 se não estiver
        '''



    def __validatePieceIn(self, node):
        '''
        Função para validar a exitência da peça no armazém superior.
        Args:
            node (tuple): nó a verificar a existência da peça

        Return:
            True: Peça existe no armazém. False: Peça não existe no armazém.
        '''
        if cur_pieces_top_wh[node[0]] == 0:
            return False
        else:
            return True



    def __validatePath(self, nodes):
        '''
        Função que verfica para cada caminho se é possível alguma transformação
        Args:
            nodes (list): lista de nós

        Return:
            transform (list): lista com a transformação possível
            Exception NoPieceInWarehouse: Não existem peças no armazém para nenhuma das transformações.
        '''
        transform = [None]*2
        updatePiecesTopWh()
        for i in range(0, len(nodes)):
            # verificar se a peça está no armazém
            if self.__validatePieceIn(nodes[i]) == False:
                if i == len(nodes)-1:
                    return -1
            else:
                transform[0] = nodes[i][0] # peça inicial
                transform[1] = nodes[i][1] # peça final
                break



    def schedule(self, G_simple: nx.DiGraph, G: nx.MultiDiGraph, target_piece, recipe=None):
        '''
        Função para agendar a produção de peças. Se recipe=None, 
        procura o caminho mais curto para a peça a produzir a partir do armazém.
        Caso contrário, utiliza a receita para encontrar o caminho mais 
        curto a partir da peça presente na receita.
        Args:
            G_simple (nx.DiGraph): grafo simples da fábrica
            G (nx.MultiDiGraph): grafo da fábrica
            client (PLCCommunications): objecto cliente OPC-UA
            piece (str): peça a produzir
            recipe (Recipe): receita a enviar para o PLC. Default: None

        Return:
            Recipe: receita a enviar para o PLC.
            Exception NoSimplePathsFound: Não foi encontrado nenhum caminho simples.
            Exception NoPieceInWarehouse: Peça não existe no armazém.
        '''
        # verificar se há receita
        if recipe is None:
            # procurar o caminho mais curto com base nas trasformações possíveis
            # só tem em conta a transformação e não os atributos como, por exemplo,
            # o tempo de transformação
            nodes, edges = findSimpleTransformations(G_simple, target_piece)

        else:
            source_piece = recipe.piece_in
            nodes, edges = findSimpleTransformations(G_simple, target_piece)

        if len(nodes) == 0 or len(edges) == 0:
            raise NameError(f"{bcolors.BOLD+bcolors.FAIL}[ERROR]{bcolors.ENDC+bcolors.ENDC}: No simple paths or edges have been found!", name="NoSimplePathsFound")

        if self.__validatePath(nodes) == -1:
            raise NameError(f"{bcolors.BOLD+bcolors.FAIL}[ERROR]{bcolors.ENDC+bcolors.ENDC}: No piece type available in warehouse!", name="NoPieceInWarehouse")
        else:
            transform = self.__validatePath(nodes)
        
        # é possível realizar a transformação. Atualiza pesos das arestas.
        self.__calculateEdgesWeights(G)

        # escolher o caminho mais curto
        shortest_path = nx.shortest_path(G, source=transform[0], target=transform[1], weight='weight', method='dijkstra')
        
        # obter todas as arestas do grafo
        all_edges = sorted(G.edges(data=True, keys=True), key=lambda x: x[3]['weight'])

        # Filtrar as arestas que estão no caminho mais curto
        edges = [(u, v, k, d) for u, v, k, d in all_edges if (u, v) in zip(shortest_path, shortest_path[1:])]

        recipe.machine_id = edges[0][3]['machine_id']
        recipe.tool = edges[0][3]['tool']
        recipe.time = edges[0][3]['time']

        # retorna 
        recipe = {"recipe_id": recipe.recipe_id, "machine_id": recipe.machine_id, "piece_in": recipe.piece_in, "tool": recipe.tool, "time": recipe.time}

        return recipe
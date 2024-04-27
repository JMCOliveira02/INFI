import modules.communications.plc_communications as plc
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



def calculateEdgesWeights(G, client: plc.PLCCommunications):
    '''
    Função para calcular o peso de todas as arestas com base no tempo de transformação, 
    tempo de mudança de ferramenta (se necessário), tempo de manutenção (se necessário),
    e prioridade de transformação das máquinas de id par.
    Args:
        G (nx.MultiDiGraph): grafo da fábrica
        client (PLCCommunications): objecto cliente OPC-UA

    Return:
        None
    '''
    # atualizar estado das máquinas
    updateMachinesState(client=client)
    # atualizar ferramenta das máquinas
    updateMachineTool(client=client)

    # cálculo do peso para cada edge
    for edge in G.edges(data=True, keys=True):
        edge_time, tool_time, main_time, previous_machine_time = 0, 0, 0, 0
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
        edge_weight = edge_time + tool_time + main_time + previous_machine_time
        G[edge[0]][edge[1]][edge[0]+edge[1]+"M"+str(edge[3]["machine_id"])]['weight'] = edge_weight
    return



def updateMachinesState(client: plc.PLCCommunications):
    '''
    Função para atualizar o estado das máquinas.
    Args:
        client (PLCCommunication): objecto cliente OPC-UA

    Return:
        None
    '''
    for i, state in enumerate(cur_machine_state):
        cur_machine_state[state] = client.getMachineState(i+1) # No PLC as máquinas não têm ID 0, mas sim de 1 a 12



def updateMachineTool(client: plc.PLCCommunications):
    '''
    Função para verificar a ferramenta atual da máquina.
    Args:
        client (PLCCommunication): objecto cliente OPC-UA

    Return:
        None
    '''
    for i, tool in enumerate(cur_machine_tool):
        cur_machine_tool[tool] = client.getCurrentTool(i+1) # No PLC as máquinas não têm ID 0, mas sim de 1 a 12



def updatePiecesTopWh(client: plc.PLCCommunications):
    '''
    Função para verificar a existência de peças no armazém superior.
    Args:
        client (PLCCommunication): objecto cliente OPC-UA

    Return:
        None
    '''
    for i, piece in enumerate(cur_pieces_top_wh):
        cur_pieces_top_wh[piece] = client.getPieceTopWH(i+1) # As peças não têm tipo 0, mas sim de 1 a 9
         


def verifyPreviousMachine(edge):
    '''
    Função para verificar se a máquina anterior está ocupada.
    Args:
        edge (tuple): aresta do grafo a verificar a máquina anterior

    Return:
        Transformations.Tmain: Máquina anterior está ocupada. 0 se não estiver
    '''



def validatePieceIn(node):
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



def chooseMachine():
    '''
    Função para escolher a máquina a utilizar. Prioridade para máquina de ID par
    Args:
        None

    Return:
        Recipe: receita a enviar para o PLC.
    '''



def schedule(G_simple: nx.DiGraph, G: nx.MultiDiGraph, client, piece, recipe=None):
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
        nodes, edges = findSimpleTransformations(G_simple, piece)
        if len(nodes) == 0 or len(edges) == 0:
            raise NameError("No simple paths or edges have been found!", name="NoSimplePathsFound")

        # verficar para cada caminho se é possível alguma transformação
        transform = [None]*2
        updatePiecesTopWh(client)
        for i in range(0, len(nodes)):
            # verificar se a peça está no armazém
            if validatePieceIn(nodes[i]) == False:
                if i == len(nodes)-1:
                    raise NameError("No piece type available in warehouse!", name="NoPieceInWarehouse")
            else:
                transform[0] = nodes[i][0] # peça inicial
                transform[1] = nodes[i][1] # peça final
                break
        
        # é possível realizar a transformação. Atualiza pesos das arestas.
        calculateEdgesWeights(G, client)
        # escolher o caminho mais curto
        shortest_path = nx.shortest_path(G, source=transform[0], target=transform[1], weight='weight', method='dijkstra')
        # obter todas as arestas do grafo
        all_edges = sorted(G.edges(data=True, keys=True), key=lambda x: x[3]['weight'])

        # Filtrar as arestas que estão no caminho mais curto
        edges = [(u, v, k, d) for u, v, k, d in all_edges if (u, v) in zip(shortest_path, shortest_path[1:])]

        print("Caminho mais curto:", shortest_path)
        print("Arestas correspondentes:", edges)
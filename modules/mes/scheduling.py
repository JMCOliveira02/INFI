import datetime

from modules.communications.plc_communications import PLCCommunications
from modules.mes.transformations import *
from modules.shopfloor.recipes import Recipe
from utils import date_diff_in_Seconds




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

# Número de peças para cada tipo disponíveis no armazém superior
cur_pieces_top_wh = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None
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
    def __init__(self, opcua_client: PLCCommunications, G: nx.MultiDiGraph, G_simple: nx.DiGraph):
        self.client = opcua_client
        self.G = G
        self.G_simple = G_simple



    def __calculateEdgesWeights(self, transform: list, is_even: bool = True):
        '''
        Função para calcular o peso de todas as arestas com base no tempo de transformação, 
        tempo de mudança de ferramenta (se necessário), tempo de manutenção (se necessário),
        se a respetiva máquina está a operar e prioridade de transformação das máquinas de id par.
        Args:
            transform: lista dos dois nós obtidos das transformações simples. Deste modo evita-se calcular
            pesos para arestas que não têm interesse para esta transformação.
            is_even: se True, a prioridade de transformação é para as máquinas de índice par.

        Return:
            -1: Todas as máquinas estão ocupadas. É melhor esperar.
            0: Existe pelo menos uma máquina livre.
        '''
        # atualizar estado das máquinas
        updateMachinesState(self.client)
        # atualizar ferramenta das máquinas
        updateMachineTool(self.client)
        busy_machines = 0
        n_edges = 0
        # cálculo do peso para cada edge
        for edge in self.G.edges(data=True, keys=True):
            if edge[0] != transform[0] or edge[1] != transform[1]:
                continue
            # atualizar número de edges válidos para esta transformação
            if is_even and edge[3]['machine_id'] % 2 == 0: # prioridade para as máquinas de índice par
                n_edges += 1 # para saber quantas arestas existem e comparar com o número de máquinas ocupadas
            elif not is_even and edge[3]['machine_id'] % 2 != 0: # prioridade para as máquinas de índice ímpar
                n_edges += 1

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
                if is_even and edge[3]['machine_id'] % 2 == 0: # prioridade para as máquinas de índice par
                    busy_machines += 1
                elif not is_even and edge[3]['machine_id'] % 2 != 0:
                    busy_machines += 1
        
            # tempo de máquina anterior (verificar se máquina anterior, de índice impar está ocupada)
            if edge[3]['machine_id'] % 2 == 0: # máquina de índice par
                if cur_machine_state[edge[3]['machine_id'] - 1] == 0: # máquina anterior (índice ímpar) não está a produzir
                    previous_machine_time = Tprevious_free
                else:
                    previous_machine_time = Tprevious_busy
            
            # cálculo do peso
            edge_weight = edge_time + tool_time + main_time + machine_time + previous_machine_time
            self.G[edge[0]][edge[1]][str(edge[0])+str(edge[1])+"M"+str(edge[3]["machine_id"])]['weight'] = edge_weight
        
        if busy_machines == n_edges:
            # indica que todas as máquinas estão ocupadas. É melhor esperar
            return -1
        return 0



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
        Função que verfica para cada caminho se é possível alguma transformação. Valida a existência de
        piece_in no armazém superior.
        Args:
            nodes (list): lista de nós

        Return:
            transform (list): lista com a transformação possível
        '''
        updatePiecesTopWh(self.client)
        for node in nodes:
            if self.__validatePieceIn(node):
                return [node[0], node[1]]  # Retorna a transformação válida
        return -1  # Retorna -1 se nenhuma transformação válida for encontrada



    def schedule(self, recipe: Recipe, status: str, is_even: bool = True):
        '''
        Função para agendar a produção de peças. Se recipe=None, 
        procura o caminho mais curto para a peça a produzir a partir do armazém.
        Caso contrário, utiliza a receita para encontrar o caminho mais 
        curto a partir da peça presente na receita.
        Args:
            recipe (Recipe): receita a enviar para o PLC. Default: None
            status (str): estado da receita ("active", "stashed", "waiting")
            is_even (bool): se True, a prioridade de transformação é para as máquinas de índice par.

        Return:
            Recipe: receita a enviar para o PLC.
            -1: Todas as máquinas estão ocupadas. É melhor esperar.
            -2: Não existe caminho possível para a peça a produzir.
            -3: Dos caminhos possíveis, nenhum é válido. Ou seja, não existe peça no armazém.
        '''
        # procurar o caminho mais curto com base nas trasformações possíveis
        # só tem em conta a transformação e não os atributos como, por exemplo,
        # o tempo de transformação. É necessário executar esta operação para receitas sem piece_out
        if status in {"waiting", "stashed"}:
            nodes, edges = findSimpleTransformations(self.G_simple, recipe.target_piece if status == "waiting" else recipe.piece_out)
            recipe.sended_date = datetime.datetime.now() if status == "waiting" else recipe.sended_date
            recipe.finished_date = datetime.datetime.now() if status == "waiting" else recipe.finished_date
            if len(nodes) == 0 or len(edges) == 0:
                return -2
            if status == "waiting":
                transform = self.__validatePath(nodes)
                if transform == -1:
                    return -3
        elif status == "active":
            nodes, edges = findSimpleTransformations(self.G_simple, recipe.target_piece, recipe.piece_out)
            transform = [nodes[0][0], nodes[0][1]]
            if len(nodes) == 0 or len(edges) == 0:
                return -2
        
        # é possível realizar a transformação. Atualiza pesos das arestas.
        all_machines_busy = self.__calculateEdgesWeights(transform, is_even)

        if all_machines_busy == -1:
            return all_machines_busy

        # escolher o caminho mais curto
        shortest_path = nx.shortest_path(self.G, source=transform[0], target=transform[1], weight='weight', method='dijkstra')
        # obter todas as arestas do grafo
        all_edges = sorted(self.G.edges(data=True, keys=True), key=lambda x: x[3]['weight'])

        # Filtrar as arestas que estão no caminho mais curto e que possuem os nós da transformação
        edges = [(u, v, k, d) for u, v, k, d in all_edges if (u, v) in zip(shortest_path, shortest_path[1:])]

        # filtrar de acordo com a prioridade de transformação
        if is_even:
            edges = [edge for edge in edges if edge[3]['machine_id'] % 2 == 0]
        else:
            edges = [edge for edge in edges if edge[3]['machine_id'] % 2 != 0]

        recipe.machine_id = edges[0][3]['machine_id']
        recipe.piece_in = edges[0][0]
        recipe.piece_out = edges[0][1]
        recipe.tool = edges[0][3]['tool']
        recipe.time = edges[0][3]['time']
        recipe.end = False
        recipe.current_transformation = (edges[0][0], edges[0][1])
        recipe.finished_date = recipe.sended_date + datetime.timedelta(seconds=date_diff_in_Seconds(recipe.finished_date, recipe.sended_date)) + datetime.timedelta(seconds=edges[0][3]["weight"]/1000)
        # recipe.in_production = True

        return recipe
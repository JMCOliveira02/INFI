import datetime

from communications.plc_communications import PLCCommunications
from mes.transformations import *
from shopfloor.recipes import Recipe
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



    def __calculateEdgesWeights(self, transform: list, active_recipes: list):
        '''
        Função para calcular o peso de todas as arestas com base no tempo de transformação, 
        tempo de mudança de ferramenta (se necessário), tempo de manutenção (se necessário),
        se a respetiva máquina está a operar e prioridade de transformação das máquinas de id par.
        Args:
            transform: lista dos dois nós obtidos das transformações simples. Deste modo evita-se calcular
            pesos para arestas que não têm interesse para esta transformação.
            active_recipes: lista de receitas ativas

        Return:
            result: lista com dois valores booleanos. Para um determinado par de nós, o primeiro indica se todas as máquinas pares estão ocupadas. 
                    O segundo indica se todas as máquinas ímpares estão ocupadas.
        '''
        # atualizar estado das máquinas
        updateMachinesState(self.client)
        # atualizar ferramenta das máquinas
        updateMachineTool(self.client)
        busy_machines_even = 0
        busy_machines_odd = 0
        n_edges_even = 0
        n_edges_odd = 0
        edges = []
        # cálculo do peso para cada edge
        for edge in self.G.edges(transform[0], data=True, keys=True):
            if edge[1] != transform[1]:
                continue
            edges.append(edge)
            # atualizar número de edges válidos para esta transformação
            if edge[3]['machine_id'] % 2 == 0: # máquinas de índice par
                n_edges_even += 1 # para saber quantas arestas existem e comparar com o número de máquinas ocupadas
            else: # máquinas de índice ímpar
                n_edges_odd += 1

            edge_time, tool_time, main_time, machine_time, previous_machine_time = 0, 0, 0, 0, 0
            # tempo de transformação
            edge_time = edge[3]['time']
            # tempo de mudança de ferramenta
            tool_time = Ttool if cur_machine_tool[edge[3]['machine_id']] != edge[3]['tool'] else 0 # No PLC as máquinas não têm ID 0, mas sim de 1 a 12
            # tempo de manutenção (verificar estado da máquina)
            main_time = Tmain if cur_machine_state[edge[3]['machine_id']] == 3 else 0
            # tempo de máquina atual (verificar se máquina está a operar)
            if cur_machine_state[edge[3]['machine_id']] == 1:
                machine_time = Tmachine
                if edge[3]['machine_id'] % 2 == 0: # prioridade para as máquinas de índice par
                    busy_machines_even += 1
                else:
                    busy_machines_odd += 1
            else:
                # tempo de máquina anterior (verificar se máquina anterior, de índice impar está ocupada)
                if edge[3]['machine_id'] % 2 == 0: # máquina de índice par
                    if cur_machine_state[edge[3]['machine_id'] - 1] == 0: # máquina anterior (índice ímpar) não está a produzir
                        previous_machine_time = Tprevious_free
                    else:
                        # ordernar as receitas que possuem máquina ímpar por tempo restante de produção (?? OLHAR PARA A TRANSFORMAÇÃO E VERIFICAR SE É A ULTIMA???)
                        odd_recipes = []
                        for recipe in active_recipes:
                            if recipe is None:
                                continue
                            if recipe.machine_id % 2 != 0:
                                odd_recipes.append(recipe)
                        odd_recipes.sort(key=lambda x: date_diff_in_Seconds(x.finished_date, datetime.datetime.now())) 
                        # encontrar índice da receita que possui a máquina ímpar
                        m = next((i) for i, recipe in enumerate(odd_recipes) if (edge[3]['machine_id'] - 1) == recipe.machine_id)
                        previous_machine_time = Tprevious_busy - 2000 * m
            
            # cálculo do peso
            edge_weight = edge_time + tool_time + main_time + machine_time + previous_machine_time
            self.G[edge[0]][edge[1]][str(edge[0])+str(edge[1])+"M"+str(edge[3]["machine_id"])]['weight'] = edge_weight
        
        result = [False, False]
        if busy_machines_even == n_edges_even:
            result[0] = True # indica que todas as máquinas pares estão ocupadas. É melhor esperar
        if busy_machines_odd == n_edges_odd:
            result[1] = True # indica que todas as máquinas ímpares estão ocupadas. É melhor esperar
        edges = -1 if result[0] and result[1] else edges
        return result, edges



    def __validatePieceIn(self, node, reserved_pieces: list):
        '''
        Função para validar a exitência da peça no armazém superior.
        Args:
            node (tuple): nó a verificar a existência da peça
            reserved_pieces (list): lista de peças reservadas para receitas stash

        Return:
            True: Peça existe no armazém. False: Peça não existe no armazém.
        '''
        if cur_pieces_top_wh[node[0]] == 0 or node[0] in reserved_pieces:
            return False
        else:
            return True



    def __validatePath(self, nodes, stashed_recipes: list):
        '''
        Função que verfica para cada caminho se é possível alguma transformação. Valida a existência de
        piece_in no armazém superior.
        Args:
            nodes (list): lista de nós
            stashed_recipes (list): lista de receitas stashed

        Return:
            transform (list): lista com a transformação possível
        '''
        reserved_pieces = []
        if len(stashed_recipes) > 0: # verificar se existem receitas stashed. Se sim, verificar quais as peças que estão reservadas
            for recipe in stashed_recipes:
                reserved_pieces.append(recipe.piece_in)

        updatePiecesTopWh(self.client)
        for node in nodes:
            if self.__validatePieceIn(node, reserved_pieces):
                return [node[0], node[1]]  # Retorna a transformação válida
        return -1  # Retorna -1 se nenhuma transformação válida for encontrada



    def schedule(self, recipe: Recipe, status: str, active_recipes: list, stashed_recipes: list):
        '''
        Função para agendar a produção de peças. Se recipe=None, 
        procura o caminho mais curto para a peça a produzir a partir do armazém.
        Caso contrário, utiliza a receita para encontrar o caminho mais 
        curto a partir da peça presente na receita.
        Args:
            recipe (Recipe): receita a enviar para o PLC. Default: None
            status (str): estado da receita ("active", "stashed", "waiting")
            active_recipes (list): lista de receitas ativas
            stashed_recipes (list): lista de receitas stashed

        Return:
            Recipe: receita a enviar para o PLC.
            -1: Todas as máquinas estão ocupadas. É melhor esperar.
            -2: Não existe caminho possível para a peça a produzir.
            -3: Dos caminhos possíveis, nenhum é válido. Ou seja, não existe peça no armazém.
        '''
        transform = []
        if status in {"waiting", "stashed"}:
            if status == "waiting":
                nodes, edges = findSimpleTransformations(self.G_simple, recipe.target_piece) # não é necessário calcular a transofrmação para receitas stashed
                if len(nodes) == 0 or len(edges) == 0:
                    return -2
                recipe.sended_date = datetime.datetime.now()
                recipe.finished_date = datetime.datetime.now()
                transform = self.__validatePath(nodes, stashed_recipes)
                if transform == -1:
                    return -3
            else:
                transform = [recipe.piece_in, recipe.piece_out] # caso a receita esteja stashed, a transformação é a mesma da receita (calculada antes de ficar stashed)
        elif status == "active":
            nodes, edges = findSimpleTransformations(self.G_simple, recipe.target_piece, recipe.piece_out)
            recipe.piece_in = nodes[0][0] # caso não encontre máquina, receita enviada para o plc fica em stash. Por isso, é necessário enviar a piece_in correta
            recipe.piece_out = nodes[0][1]
            recipe.tool = 0
            recipe.time = 0
            recipe.current_transformation = (nodes[0][0], nodes[0][1])
            recipe.end = False
            transform = [nodes[0][0], nodes[0][1]]
            if len(nodes) == 0 or len(edges) == 0:
                return -2
        
        # é possível realizar a transformação. Atualiza pesos das arestas.
        all_machines_busy, all_edges = self.__calculateEdgesWeights(transform, active_recipes)
        
        if all_machines_busy[0] and all_machines_busy[1]:
            return -1
        
        sorted_edges = sorted(all_edges, key=lambda x: x[3]['weight'])

        edge_ = []
        for edge in sorted_edges:
            if not all_machines_busy[0] and edge[3]['machine_id'] % 2 == 0: # máquina de indice par
                edge_ = edge
                break
            elif all_machines_busy[0] and not all_machines_busy[1] and edge[3]['machine_id'] % 2 != 0: # máquina de indice ímpar
                edge_ = edge
                break

        recipe.machine_id = edge_[3]['machine_id']
        recipe.piece_in = edge_[0]
        recipe.piece_out = edge_[1]
        recipe.tool = edge_[3]['tool']
        recipe.time = edge_[3]['time']
        recipe.end = False
        recipe.current_transformation = (edge_[0], edge_[1])
        end_time_prediction = (recipe.time + (Ttool if recipe.tool != cur_machine_tool[recipe.machine_id] else 0)) / 1000 # tempo de transformação + tempo de mudança de ferramenta se ferramenta a utilziar for diferente da atual
        recipe.finished_date = recipe.sended_date + datetime.timedelta(seconds=date_diff_in_Seconds(recipe.finished_date, recipe.sended_date)) + datetime.timedelta(seconds=end_time_prediction)

        return recipe
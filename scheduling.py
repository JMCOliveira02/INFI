import networkx as nx
import transformations as tf
import plc_communications as plc



def generateGraph():
    '''
    Função que gera o grafo da fábrica
    args:
        edges (list): lista com informação sobre os vertíces

    Returns:
        nx.MultiDiGraph: grafo da fábrica
    '''
    G = nx.MultiDiGraph()

    #for node in nodes:
    #    G.add_node(node)

    for edge in tf.edges:
        #           peça1    peça2      peso            tempo       ferramenta       id_máquina
        G.add_edge(edge[0], edge[1], weight=edge[2], time=edge[3], tool=edge[4], machine_id=edge[5])
    
    return G



def findTransformations(G, piece):
    '''
    Função que encontra as transformações possíveis para uma peça e devolve os caminhos e arestas possíveis ordenadas

    args:
        G (nx.MultiDiGraph): grafo da fábrica
        piece (str): peça a transformar

    Returns:
        list, list: lista com caminhos possíveis, lista com arestas possíveis
    '''
    all_nodes = []
    all_edges = []
    for node in G.nodes():
        if node != piece:
            for path in nx.all_simple_paths(G, source=node, target=piece):
                all_nodes.append(path)
            for edge in sorted(nx.all_simple_edge_paths(G, source=node, target=piece)):
                all_edges.append(edge)

    # Verificar se é possível fazer a transformação
    if len(all_nodes) == 0 or len(all_edges) == 0:
        #print("No paths or edges have been found!")
        return [], []

    all_nodes, all_edges = sortTransformations(G, all_nodes, all_edges)

    return all_nodes, all_edges    



def sortTransformations(G, nodes, edges):
    '''
    Função que calcula os nós e vertíces possíveis com base num grafo por ordem 
    crescente do tempo total de cada caminho

    args:
        G (nx.MultiDiGraph): grafo da fábrica
        nodes (list): lista com caminhos possíveis
        edges (list): lista com arestas possíveis

    Returns:
        list, list: lista com caminhos possíveis ordenados, lista com arestas possíveis ordenadas
    '''
    edges_ = []

    # Somar o tempo de cada aresta para cada caminho
    for edge in edges:
        time = 0
        # Para cada aresta no caminho
        for i in range(len(edge)):
            # Somar o tempo da aresta ao tempo total
            time += G.get_edge_data(edge[i][0], edge[i][1], key=edge[i][2])['time']
        edges_.append((edge, time))

    # Obter indices ordenados
    sorted_edges_ = sorted(range(len(edges_)), key=lambda k: edges_[k][1])

    # Ordenar as arestas por tempo
    #edges_ = [edges_[i] for i in sorted_edges_]
    edges = [edges[i] for i in sorted_edges_]
    # Ordenar os caminhos por tempo
    #sorted_nodes = [nodes[i] for i in sorted_edges_]
    nodes = [nodes[i] for i in sorted_edges_]

    return nodes, edges



def calculateEdgeWeight(edge):
    '''
    Função para calcular o peso de uma aresta com base no tempo de transformação, 
    tempo de mudança de ferramenta (se necessário), tempo de manutenção (se necessário),
    e prioridade de transformação das máquinas de id par.
    Args:
        edge (tuple): aresta do grafo a calcular o peso

    Return:
        weight: peso da aresta
    '''
      
    # tempo de transformação
    edge_time = edge[3]
    # tempo de mudança de ferramenta
    tool_time = verifyCurrentTool(edge)
    # tempo de manutenção (verificar estado da máquina)
    #main_time = verifyMachineState(edge)
    # tempo de máquina anterior (verificar se máquina anterior está ocupada) 
    #previous_machine_time = verifyPreviousMachine(edge)

    return edge_time + tool_time



def verifyCurrentTool(edge):
    '''
    Função para verificar a ferramenta atual da máquina.
    Args:
        edge (tuple): aresta do grafo a verificar a ferramenta

    Return:
        Transformations.Ttool: Ferramenta atual é a incorreta. 0 se for a correta
    '''


def verifyMachineState(edge):
    '''
    Função para verificar o estado da máquina.
    Args:
        edge (tuple): aresta do grafo a verificar o estado da máquina

    Return:
        Transformations.Tmain: Máquina está em manutenção. 0 se não estiver
    '''


def verifyPreviousMachine(edge):
    '''
    Função para verificar se a máquina anterior está ocupada.
    Args:
        edge (tuple): aresta do grafo a verificar a máquina anterior

    Return:
        Transformations.Tmain: Máquina anterior está ocupada. 0 se não estiver
    '''



def validatePieceIn():
    '''
    Função para validar a exitência da peça no armazém superior.
    Args:
        None

    Return:
        True: Peça existe no armazém. False: Peça não existe no armazém.
    '''



def chooseMachine():
    '''
    Função para escolher a máquina a utilizar. Prioridade para máquina de ID par
    Args:
        None

    Return:
        Recipe: receita a enviar para o PLC.
    '''



def schedule(G, piece):
    '''
    Função para agendar a produção de peças.
    Args:
        G (nx.MultiDiGraph): grafo da fábrica
        piece (str): peça a produzir

    Return:
        None
    '''
    nodes, edges = findTransformations(G, piece)

    if len(nodes) == 0 or len(edges) == 0:
        print("No paths or edges have been found!")
        return
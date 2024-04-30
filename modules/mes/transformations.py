import networkx as nx
from utils import bcolors



# **********Variáveis de configuração**********

Ttool = 30000 # tempo de mudança de ferramenta, ms
Tmain = 9999999999 # tempo de manutenção, ms
Tmachine = 30000 # tempo de máquina, ms
Tprevious_busy = 30000 # tempo de máquina anterior, ms
Tprevious_free = -15000

nodes = [
    # peça 1, peça 2
    ('P1', 'P3'),
    ('P4', 'P6'),
    ('P2', 'P8'),
    ('P3', 'P4'),
    ('P4', 'P7'),
    ('P4', 'P5'),
    ('P8', 'P9'),
    ('P8', 'P7')
]

# arestas para grafo simplificado
simple_edges = [
    # nó 1, nó 2, ferramenta, tempo
    ('P1', 'P3', "T1", 45000),
    ('P4', 'P6', "T2", 25000),
    ('P2', 'P8', "T1", 45000),
    ('P3', 'P4', "T2", 15000),
    ('P3', 'P4', "T3", 25000),
    ('P4', 'P7', "T3", 15000),
    ('P4', 'P5', "T4", 25000),
    ('P8', 'P9', "T5", 45000),
    ('P8', 'P7', "T6", 15000)
]

# arestas para grafo completo
edges = [
    # peça 1, peça 2, peso(começa com valor 1), tempo, ferramenta, id_máquina

    # Transformação P1 -> P3 com T1 ocorre em todas as máquinas com tempo 45000
    ('P1', 'P3', 1, 45000, 1, 1),
    ('P1', 'P3', 1, 45000, 1, 2),
    ('P1', 'P3', 1, 45000, 1, 3),
    ('P1', 'P3', 1, 45000, 1, 4),
    ('P1', 'P3', 1, 45000, 1, 5),
    ('P1', 'P3', 1, 45000, 1, 6),
    ('P1', 'P3', 1, 45000, 1, 7),
    ('P1', 'P3', 1, 45000, 1, 8),
    ('P1', 'P3', 1, 45000, 1, 9),
    ('P1', 'P3', 1, 45000, 1, 10),
    ('P1', 'P3', 1, 45000, 1, 11),
    ('P1', 'P3', 1, 45000, 1, 12),

    # Transformação P3 -> P4 com T2 ocorre nas máquinas 1 a 6 com tempo 15000
    ('P3', 'P4', 1, 15000, 2, 1),
    ('P3', 'P4', 1, 15000, 2, 2),
    ('P3', 'P4', 1, 15000, 2, 3),
    ('P3', 'P4', 1, 15000, 2, 4),
    ('P3', 'P4', 1, 15000, 2, 5),
    ('P3', 'P4', 1, 15000, 2, 6),

    # Transformação P3 -> P4 com T3 ocorre nas máquinas 1 a 6 com tempo 25000
    ('P3', 'P4', 1, 25000, 3, 1),
    ('P3', 'P4', 1, 25000, 3, 2),
    ('P3', 'P4', 1, 25000, 3, 3),
    ('P3', 'P4', 1, 25000, 3, 4),
    ('P3', 'P4', 1, 25000, 3, 5),
    ('P3', 'P4', 1, 25000, 3, 6),

    # Transformação P4 -> P5 com T4 ocorre nas máquinas 7 a 12 com tempo 25000
    ('P4', 'P5', 1, 25000, 4, 7),
    ('P4', 'P5', 1, 25000, 4, 8),
    ('P4', 'P5', 1, 25000, 4, 9),
    ('P4', 'P5', 1, 25000, 4, 10),
    ('P4', 'P5', 1, 25000, 4, 11),
    ('P4', 'P5', 1, 25000, 4, 12),

    # Transformação P4 -> P6 com T2 ocorre nas máquinas 1 a 6 com tempo 25000
    ('P4', 'P6', 1, 25000, 2, 1),
    ('P4', 'P6', 1, 25000, 2, 2),
    ('P4', 'P6', 1, 25000, 2, 3),
    ('P4', 'P6', 1, 25000, 2, 4),
    ('P4', 'P6', 1, 25000, 2, 5),
    ('P4', 'P6', 1, 25000, 2, 6),

    # Transformação P4 -> P7 com T3 ocorre nas máquinas 1 a 6 com tempo 15000
    ('P4', 'P7', 1, 15000, 3, 1),
    ('P4', 'P7', 1, 15000, 3, 2),
    ('P4', 'P7', 1, 15000, 3, 3),
    ('P4', 'P7', 1, 15000, 3, 4),
    ('P4', 'P7', 1, 15000, 3, 5),
    ('P4', 'P7', 1, 15000, 3, 6),

    # Transformação P2 -> P8 com T1 ocorre em todas as máquinas com tempo 45000
    ('P2', 'P8', 1, 45000, 1, 1),
    ('P2', 'P8', 1, 45000, 1, 2),
    ('P2', 'P8', 1, 45000, 1, 3),
    ('P2', 'P8', 1, 45000, 1, 4),
    ('P2', 'P8', 1, 45000, 1, 5),
    ('P2', 'P8', 1, 45000, 1, 6),
    ('P2', 'P8', 1, 45000, 1, 7),
    ('P2', 'P8', 1, 45000, 1, 8),
    ('P2', 'P8', 1, 45000, 1, 9),
    ('P2', 'P8', 1, 45000, 1, 10),
    ('P2', 'P8', 1, 45000, 1, 11),
    ('P2', 'P8', 1, 45000, 1, 12),

    # Transformação de P8 -> P7 com T6 ocorre nas máquinas 8, 10 e 12 com tempo 15000
    ('P8', 'P7', 1, 15000, 6, 8),
    ('P8', 'P7', 1, 15000, 6, 10),
    ('P8', 'P7', 1, 15000, 6, 12),

    # transformação de P8 -> P9 com T5 ocorre nas máquinas 7, 9 e 11 com tempo 45000
    ('P8', 'P9', 1, 45000, 5, 7),
    ('P8', 'P9', 1, 45000, 5, 9),
    ('P8', 'P9', 1, 45000, 5, 11)
]

# *********************************************


def generateGraph():
    '''
    Função que gera o grafo da fábrica
    args:
        None

    Returns:
        nx.MultiDiGraph: grafo da fábrica
    '''
    G = nx.MultiDiGraph()

    # for node in nodes:
    #     G.add_node(node)

    for edge in edges:
        #           peça1    peça2                                            peso            tempo       ferramenta       id_máquina
        G.add_edge(edge[0], edge[1], key=edge[0]+edge[1]+"M"+str(edge[5]), weight=edge[2], time=edge[3], tool=edge[4], machine_id=edge[5])
    print(f"\n{bcolors.BOLD}[MES]{bcolors.ENDC}: Graph generated!")

    return G



def generateSimpleGraph():
    '''
    Função que gera o grafo simplificado da fábrica
    args:
        None

    Returns:
        nx.DiGraph: grafo simplificado da fábrica
    '''
    G = nx.DiGraph()

    # for node in nodes:
    #     G.add_node(node)

    for edge in simple_edges:
        #           peça1    peça2
        G.add_edge(edge[0], edge[1])
    print(f"\n{bcolors.BOLD}[MES]{bcolors.ENDC}: Simple graph generated!")

    return G



def generateGrahps():
    '''
    Função que gera o grafo e o grafo simplificado da fábrica
    args:
        None

    Returns:
        G (nx.MultiDiGraph), G_simple (nx.DiGraph): grafo da fábrica, grafo simplificado da fábrica
    '''
    G = generateGraph()
    G_simple = generateSimpleGraph()

    return G, G_simple



def findSimpleTransformations(G_simple, piece):
    '''
    Função que encontra as transformações possíveis para uma peça e devolve os caminhos e arestas possíveis ordenadas

    args:
        G_simple (nx.DiGraph): grafo simplificado da fábrica
        piece (str): peça a transformar

    Returns:
        all_nodes (list), all_edges (list): lista com caminhos possíveis, lista com arestas possíveis
    '''
    all_nodes = []
    all_edges = []
    for node in G_simple.nodes:
        if node != piece:
            for path in nx.all_simple_paths(G_simple, source=node, target=piece):
                all_nodes.append(path)
            for edge in sorted(nx.all_simple_edge_paths(G_simple, source=node, target=piece)):
                all_edges.append(edge)

    # Verificar se é possível fazer a transformação
    if len(all_nodes) == 0 or len(all_edges) == 0:
        #print("No paths or edges have been found!")
        return [], []

    all_nodes, all_edges = sortTransformations(G_simple, all_nodes, all_edges)

    return all_nodes, all_edges    



def sortTransformations(G, nodes, edges):
    '''
    Função que calcula os nós e vertíces possíveis com base num grafo por ordem 
    crescente do caminho mais curto

    args:
        G (nx.DiGraph): grafo da fábrica
        nodes (list): lista com caminhos possíveis
        edges (list): lista com arestas possíveis

    Returns:
        nodes (list), edges (list): lista com caminhos possíveis ordenados, lista com arestas possíveis ordenadas
    '''
    # Obter indices ordenados
    sorted_edges_ = sorted(range(len(edges)), key=lambda k: len(edges[k]))

    # Ordenar as arestas
    edges = [edges[i] for i in sorted_edges_]
    # Ordenar os caminhos
    nodes = [nodes[i] for i in sorted_edges_]

    return nodes, edges
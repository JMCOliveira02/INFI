from mes import nx

from mes import bcolors



# **********Variáveis de configuração**********

Ttool = 30000 # tempo de mudança de ferramenta, ms
Tmain = 9999999999 # tempo de manutenção, ms
Tmachine = 40000 # tempo de máquina, ms
Tprevious_busy = 30000 # tempo de máquina anterior, ms
Tprevious_free = -15000

# nodes = [
#     # peça 1, peça 2
#     ('P1', 'P3'),
#     ('P4', 'P6'),
#     ('P2', 'P8'),
#     ('P3', 'P4'),
#     ('P4', 'P7'),
#     ('P4', 'P5'),
#     ('P8', 'P9'),
#     ('P8', 'P7')
# ]

# # arestas para grafo simplificado
# simple_edges = [
#     # nó 1, nó 2, ferramenta, tempo
#     ('P1', 'P3', "T1", 45000),
#     ('P4', 'P6', "T2", 25000),
#     ('P2', 'P8', "T1", 45000),
#     ('P3', 'P4', "T2", 15000),
#     ('P3', 'P4', "T3", 25000),
#     ('P4', 'P7', "T3", 15000),
#     ('P4', 'P5', "T4", 25000),
#     ('P8', 'P9', "T5", 45000),
#     ('P8', 'P7', "T6", 15000)
# ]

# # arestas para grafo completo
# edges = [
#     # peça 1, peça 2, peso(começa com valor 1), tempo, ferramenta, id_máquina

#     # Transformação P1 -> P3 com T1 ocorre em todas as máquinas com tempo 45000
#     ('P1', 'P3', 1, 45000, 1, 1),
#     ('P1', 'P3', 1, 45000, 1, 2),
#     ('P1', 'P3', 1, 45000, 1, 3),
#     ('P1', 'P3', 1, 45000, 1, 4),
#     ('P1', 'P3', 1, 45000, 1, 5),
#     ('P1', 'P3', 1, 45000, 1, 6),
#     ('P1', 'P3', 1, 45000, 1, 7),
#     ('P1', 'P3', 1, 45000, 1, 8),
#     ('P1', 'P3', 1, 45000, 1, 9),
#     ('P1', 'P3', 1, 45000, 1, 10),
#     ('P1', 'P3', 1, 45000, 1, 11),
#     ('P1', 'P3', 1, 45000, 1, 12),

#     # Transformação P3 -> P4 com T2 ocorre nas máquinas 1 a 6 com tempo 15000
#     ('P3', 'P4', 1, 15000, 2, 1),
#     ('P3', 'P4', 1, 15000, 2, 2),
#     ('P3', 'P4', 1, 15000, 2, 3),
#     ('P3', 'P4', 1, 15000, 2, 4),
#     ('P3', 'P4', 1, 15000, 2, 5),
#     ('P3', 'P4', 1, 15000, 2, 6),

#     # Transformação P3 -> P4 com T3 ocorre nas máquinas 1 a 6 com tempo 25000
#     ('P3', 'P4', 1, 25000, 3, 1),
#     ('P3', 'P4', 1, 25000, 3, 2),
#     ('P3', 'P4', 1, 25000, 3, 3),
#     ('P3', 'P4', 1, 25000, 3, 4),
#     ('P3', 'P4', 1, 25000, 3, 5),
#     ('P3', 'P4', 1, 25000, 3, 6),

#     # Transformação P4 -> P5 com T4 ocorre nas máquinas 7 a 12 com tempo 25000
#     ('P4', 'P5', 1, 25000, 4, 7),
#     ('P4', 'P5', 1, 25000, 4, 8),
#     ('P4', 'P5', 1, 25000, 4, 9),
#     ('P4', 'P5', 1, 25000, 4, 10),
#     ('P4', 'P5', 1, 25000, 4, 11),
#     ('P4', 'P5', 1, 25000, 4, 12),

#     # Transformação P4 -> P6 com T2 ocorre nas máquinas 1 a 6 com tempo 25000
#     ('P4', 'P6', 1, 25000, 2, 1),
#     ('P4', 'P6', 1, 25000, 2, 2),
#     ('P4', 'P6', 1, 25000, 2, 3),
#     ('P4', 'P6', 1, 25000, 2, 4),
#     ('P4', 'P6', 1, 25000, 2, 5),
#     ('P4', 'P6', 1, 25000, 2, 6),

#     # Transformação P4 -> P7 com T3 ocorre nas máquinas 1 a 6 com tempo 15000
#     ('P4', 'P7', 1, 15000, 3, 1),
#     ('P4', 'P7', 1, 15000, 3, 2),
#     ('P4', 'P7', 1, 15000, 3, 3),
#     ('P4', 'P7', 1, 15000, 3, 4),
#     ('P4', 'P7', 1, 15000, 3, 5),
#     ('P4', 'P7', 1, 15000, 3, 6),

#     # Transformação P2 -> P8 com T1 ocorre em todas as máquinas com tempo 45000
#     ('P2', 'P8', 1, 45000, 1, 1),
#     ('P2', 'P8', 1, 45000, 1, 2),
#     ('P2', 'P8', 1, 45000, 1, 3),
#     ('P2', 'P8', 1, 45000, 1, 4),
#     ('P2', 'P8', 1, 45000, 1, 5),
#     ('P2', 'P8', 1, 45000, 1, 6),
#     ('P2', 'P8', 1, 45000, 1, 7),
#     ('P2', 'P8', 1, 45000, 1, 8),
#     ('P2', 'P8', 1, 45000, 1, 9),
#     ('P2', 'P8', 1, 45000, 1, 10),
#     ('P2', 'P8', 1, 45000, 1, 11),
#     ('P2', 'P8', 1, 45000, 1, 12),

#     # Transformação de P8 -> P7 com T6 ocorre nas máquinas 8, 10 e 12 com tempo 15000
#     ('P8', 'P7', 1, 15000, 6, 8),
#     ('P8', 'P7', 1, 15000, 6, 10),
#     ('P8', 'P7', 1, 15000, 6, 12),

#     # transformação de P8 -> P9 com T5 ocorre nas máquinas 7, 9 e 11 com tempo 45000
#     ('P8', 'P9', 1, 45000, 5, 7),
#     ('P8', 'P9', 1, 45000, 5, 9),
#     ('P8', 'P9', 1, 45000, 5, 11)
# ]

nodes = [
    # peça 1, peça 2
    (1, 3),
    (4, 6),
    (2, 8),
    (3, 4),
    (4, 7),
    (4, 5),
    (8, 9),
    (8, 7)
]

# arestas para grafo simplificado
simple_edges = [
    # nó 1, nó 2, ferramenta, tempo
    (1, 3, 1, 45000),
    (4, 6, 2, 25000),
    (2, 8, 1, 45000),
    (3, 4, 2, 15000),
    (3, 4, 3, 25000),
    (4, 7, 3, 15000),
    (4, 5, 4, 25000),
    (8, 9, 5, 45000),
    (8, 7, 6, 15000)
]

# arestas para grafo completo
edges = [
    # peça 1, peça 2, peso(começa com valor 1), tempo, ferramenta, id_máquina

    # Transformação P1 -> P3 com T1 ocorre em todas as máquinas com tempo 45000
    (1, 3, 1, 45000, 1, 1),
    (1, 3, 1, 45000, 1, 2),
    (1, 3, 1, 45000, 1, 3),
    (1, 3, 1, 45000, 1, 4),
    (1, 3, 1, 45000, 1, 5),
    (1, 3, 1, 45000, 1, 6),
    (1, 3, 1, 45000, 1, 7),
    (1, 3, 1, 45000, 1, 8),
    (1, 3, 1, 45000, 1, 9),
    (1, 3, 1, 45000, 1, 10),
    (1, 3, 1, 45000, 1, 11),
    (1, 3, 1, 45000, 1, 12),

    # Transformação P3 -> P4 com T2 ocorre nas máquinas 1 a 6 com tempo 15000
    (3, 4, 1, 15000, 2, 1),
    (3, 4, 1, 15000, 2, 2),
    (3, 4, 1, 15000, 2, 3),
    (3, 4, 1, 15000, 2, 4),
    (3, 4, 1, 15000, 2, 5),
    (3, 4, 1, 15000, 2, 6),

    # Transformação P3 -> P4 com T3 ocorre nas máquinas 1 a 6 com tempo 25000
    (3, 4, 1, 25000, 3, 1),
    (3, 4, 1, 25000, 3, 2),
    (3, 4, 1, 25000, 3, 3),
    (3, 4, 1, 25000, 3, 4),
    (3, 4, 1, 25000, 3, 5),
    (3, 4, 1, 25000, 3, 6),

    # Transformação P4 -> P5 com T4 ocorre nas máquinas 7 a 12 com tempo 25000
    (4, 5, 1, 25000, 4, 7),
    (4, 5, 1, 25000, 4, 8),
    (4, 5, 1, 25000, 4, 9),
    (4, 5, 1, 25000, 4, 10),
    (4, 5, 1, 25000, 4, 11),
    (4, 5, 1, 25000, 4, 12),

    # Transformação P4 -> P6 com T2 ocorre nas máquinas 1 a 6 com tempo 25000
    (4, 6, 1, 25000, 2, 1),
    (4, 6, 1, 25000, 2, 2),
    (4, 6, 1, 25000, 2, 3),
    (4, 6, 1, 25000, 2, 4),
    (4, 6, 1, 25000, 2, 5),
    (4, 6, 1, 25000, 2, 6),

    # Transformação P4 -> P7 com T3 ocorre nas máquinas 1 a 6 com tempo 15000
    (4, 7, 1, 15000, 3, 1),
    (4, 7, 1, 15000, 3, 2),
    (4, 7, 1, 15000, 3, 3),
    (4, 7, 1, 15000, 3, 4),
    (4, 7, 1, 15000, 3, 5),
    (4, 7, 1, 15000, 3, 6),

    # Transformação P2 -> P8 com T1 ocorre em todas as máquinas com tempo 45000
    (2, 8, 1, 45000, 1, 1),
    (2, 8, 1, 45000, 1, 2),
    (2, 8, 1, 45000, 1, 3),
    (2, 8, 1, 45000, 1, 4),
    (2, 8, 1, 45000, 1, 5),
    (2, 8, 1, 45000, 1, 6),
    (2, 8, 1, 45000, 1, 7),
    (2, 8, 1, 45000, 1, 8),
    (2, 8, 1, 45000, 1, 9),
    (2, 8, 1, 45000, 1, 10),
    (2, 8, 1, 45000, 1, 11),
    (2, 8, 1, 45000, 1, 12),

    # Transformação de P8 -> P7 com T6 ocorre nas máquinas 8, 10 e 12 com tempo 15000
    (8, 7, 1, 15000, 6, 8),
    (8, 7, 1, 15000, 6, 10),
    (8, 7, 1, 15000, 6, 12),

    # transformação de P8 -> P9 com T5 ocorre nas máquinas 7, 9 e 11 com tempo 45000
    (8, 9, 1, 45000, 5, 7),
    (8, 9, 1, 45000, 5, 9),
    (8, 9, 1, 45000, 5, 11)
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
        G.add_edge(edge[0], edge[1], key=str(edge[0])+str(edge[1])+"M"+str(edge[5]), weight=edge[2], time=edge[3], tool=edge[4], machine_id=edge[5])
    print(f"\n{bcolors.BOLD}[MES]{bcolors.ENDC} Graph generated!")

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
    print(f"\n{bcolors.BOLD}[MES]{bcolors.ENDC} Simple graph generated!")

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



def findSimpleTransformations(G_simple, target_piece, source_piece = None):
    '''
    Função que encontra as transformações possíveis para uma peça e devolve os caminhos e arestas possíveis ordenadas

    args:
        G_simple (nx.DiGraph): grafo simplificado da fábrica
        target_piece (int): peça a transformar
        source_piece (int): peça de origem

    Returns:
        all_nodes (list), all_edges (list): lista com caminhos possíveis, lista com arestas possíveis
    '''
    all_nodes = []
    all_edges = []
    if source_piece is not None:
        for path in nx.all_simple_paths(G_simple, source=source_piece, target=target_piece):
            all_nodes.append(path)
        for edge in nx.all_simple_edge_paths(G_simple, source=source_piece, target=target_piece):
            all_edges.append(edge)
    else:
        for node in G_simple.nodes:
            if node != target_piece:
                for path in nx.all_simple_paths(G_simple, source=node, target=target_piece):
                    all_nodes.append(path)
                for edge in nx.all_simple_edge_paths(G_simple, source=node, target=target_piece):
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
from utils import *
import networkx as nx



def generateGraph(edges):
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

    for edge in edges:
        G.add_edge(edge[0], edge[1], key=edge[0]+edge[1]+edge[2], tool=edge[2], time=edge[3])
    
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
        print("No paths or edges have been found!")
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



class Transformation:
    '''
    classe para indicar a transformação que será realizada
    '''
    def __init__(self, tool, initialPiece, finalPiece, time):
        self.tool = tool
        self.initialPiece = initialPiece
        self.finalPiece = finalPiece
        self.time = time


class Recipe:
    '''
    Classe para indicar a receita a efetuar
    '''
    def __init__(self, transformation, toolAction, machineId):
        self.initialPiece = transformation.initialPiece
        self.time = transformation.time
        self.toolAction = toolAction
        self.machineId = machineId

    def getNodes(self, client, index):
        self.idNode = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.Variables.recipes["+ str(index) + "].machine_id")
        self.pieceInNode = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.Variables.recipes["+ str(index) + "].piece_in")
        self.timeNode = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.Variables.recipes["+ str(index) + "].time_")
        self.toolActionNode = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.Variables.recipes["+ str(index) + "].tool")
        self.endNode = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.Variables.recipes["+ str(index) + "].end")


storeTransformation = Transformation(0, 0, 0, 0)
storeRecipe = Recipe(storeTransformation, 0, -1)


class M1:
    '''
    Classe que indica ferramentas e transformações das máquinas M1
    '''
    tool = [1, 2, 3]
    P1P3 = Transformation(1, 1, 3, 45000)
    P4P6 = Transformation(2, 4, 6, 25000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P3P4a = Transformation(2, 3, 4, 15000)
    P3P4b = Transformation(3, 3, 4, 25000)
    P4P7 = Transformation(3, 4, 7, 15000)

class M2:
    '''
    Classe que indica ferramentas e transformações das máquinas M2
    '''
    tool = [1, 2, 3]
    P1P3 = Transformation(1, 1, 3, 45000)
    P4P6 = Transformation(2, 4, 6, 25000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P3P4a = Transformation(2, 3, 4, 15000)
    P3P4b = Transformation(3, 3, 4, 25000)
    P4P7 = Transformation(3, 4, 7, 15000)

class M3:
    '''
    Classe que indica ferramentas e transformações das máquinas M3
    '''
    tool = [1, 4, 5]
    P1P3 = Transformation(1, 1, 3, 45000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P4P5 = Transformation(4, 4, 5, 25000)
    P8P9 = Transformation(5, 8, 9, 45000)

class M4:
    '''
    Classe que indica ferramentas e transformações das máquinas M4
    '''
    tool = [1, 4, 6]
    P1P3 = Transformation(1, 1, 3, 45000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P4P5 = Transformation(4, 4, 5, 25000)
    P8P7 = Transformation(6, 8, 7, 15000)


def sendRecipe(recipe):
    '''
    Função que envia a receita para a máquina

    Args:
        recipe (Recipe): receita a enviar
    '''
    setValueCheck(recipe.pieceInNode, recipe.initialPiece, ua.VariantType.Int16)
    setValueCheck(recipe.timeNode, recipe.time, ua.VariantType.UInt32)
    setValueCheck(recipe.toolActionNode, recipe.toolAction, ua.VariantType.Int16)
    setValueCheck(recipe.idNode, recipe.machineId, ua.VariantType.Int16)
    setValueCheck(recipe.endNode, False, ua.VariantType.Boolean)


def storePiece(client, index):
    '''

    '''
    recipe = Recipe(storeTransformation, 0, -1)
    recipe.getNodes(client, index)
    sendRecipe(recipe)
    #while recipe.endNode.get_value() == False:
    #    pass
    #setValueCheck(recipe.endNode, True, ua.VariantType.Boolean)


class Machine:
    def __init__(self, client,type, Id, activeTool):
        self.client = client
        self.line = None
        self.Id = Id
        self.type = type
        self.activeTool = activeTool

    def performTransformation(self, transformation, index):

        toolAction = self.calcToolAction(transformation)

        recipe = Recipe(transformation, toolAction, self.Id)
        recipe.getNodes(self.client, index)

        sendRecipe(recipe)
        while recipe.endNode.get_value() == False:
            pass
        setValueCheck(recipe.endNode, False, ua.VariantType.Boolean)

    def calcToolAction(self, chosenTransformation):
        transformationToolIndex = self.type.tool.index(chosenTransformation.tool) + 1
        print(chosenTransformation.tool, transformationToolIndex, self.activeTool)
        activeToolIndex = self.type.tool.index(self.activeTool) + 1

        print(transformationToolIndex, activeToolIndex)
        if(activeToolIndex == transformationToolIndex):
            return 0
        if(activeToolIndex == 1):
            if(transformationToolIndex == 2):
                return 1
            if(transformationToolIndex == 3):
                return -1
        if(activeToolIndex == 2):
            if(transformationToolIndex == 1):
                return -1
            if(transformationToolIndex == 3):
                return 1
        if(activeToolIndex == 3):
            if(transformationToolIndex == 1):
                return 1
            if(transformationToolIndex == 2):
                return -1

    def findTransformations(self, piece):
        '''
        Função que encontra as transformações possíveis para uma peça

        args:
            piece (int): peça a transformar
        '''
        return [transformation for transformation in self.type.__dict__.values() if isinstance(transformation, Transformation) and transformation.finalPiece == piece]


def chooseTransformation(transformations):
    '''
    Função que escolhe a melhor transformação a realizar

    args:
        transformations (dict): dicionário com as transformações possíveis para cada máquina
    '''
    min_time = float('inf')
    best_machine_id = None
    best_transformation = None
    for machine_id in range(len(transformations)):
        for transformation in transformations[machine_id]:
            if transformation.time < min_time:
                min_time = transformation.time
                best_machine_id = machine_id
                best_transformation = transformation
            elif transformation.time == min_time and machine_id < best_machine_id:
                best_machine_id = machine_id
                best_transformation = transformation
    return best_machine_id + 1, best_transformation
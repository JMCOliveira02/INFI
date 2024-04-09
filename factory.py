class Transformation:
    def __init__(self, tool, initialPiece, finalPiece, time):
        self.tool = tool
        self.initialPiece = initialPiece
        self.finalPiece = finalPiece
        self.time = time

class M1:
    tool = [1, 2, 3]
    P1P3 = Transformation(1, 1, 3, 45000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P3P4a = Transformation(2, 3, 4, 15000)
    P3P4b = Transformation(3, 3, 4, 25000)
    P4P7 = Transformation(3, 4, 7, 15000)
        
class M2:
    tool = [1, 2, 3]
    P1P3 = Transformation(1, 1, 3, 45000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P3P4a = Transformation(2, 3, 4, 15000)
    P3P4b = Transformation(3, 3, 4, 25000)
    P4P7 = Transformation(3, 4, 7, 15000)

class M3:
    tool = [1, 4, 5]
    P1P3 = Transformation(1, 1, 3, 45000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P4P5 = Transformation(4, 4, 5, 25000)
    P8P9 = Transformation(5, 8, 9, 45000)

class M4:
    tool = [1, 4, 6]
    P1P3 = Transformation(1, 1, 3, 45000)
    P2P8 = Transformation(1, 2, 8, 45000)
    P4P5 = Transformation(4, 4, 5, 25000)
    P8P7 = Transformation(6, 8, 7, 15000)


class Machine:
    def __init__(self, client,type, Id, activeTool):
        self.client = client
        self.line = None
        self.Id = Id
        self.type = type
        self.activeTool = self.type.tool[activeTool]

    def sendRecipe(self, transformation):
        initialPiece = transformation.initialPiece
        finalPiece = transformation.finalPiece
        time = transformation.time
        tool = transformation.tool
        machineID = self.Id


class Recipe:
    def __init__(self, transformation, tool, machine):
        self.initialPiece = transformation.initialPiece
        self.finalPiece = transformation.finalPiece
        self.time = transformation.time
        self.tool = tool
        self.machine = machine


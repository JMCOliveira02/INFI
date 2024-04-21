from opcua import Client
from opcua import ua
from utils import *

class Cin:
    def __init__(self, client, Id):
        self.client = client
        self.piece = None
        self.numPieces = None
        self.enable = None
        self.finished = None
        self.Id = Id

    def get_nodes(self):
        self.piece = self.client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PGR_wh_in.Cin"+ str(self.Id) + ".piece")
        self.numPieces = self.client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PGR_wh_in.Cin" + str(self.Id) + ".num_pieces")
        self.enable = self.client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PGR_wh_in.Cin" + str(self.Id) + ".recv_I")
        self.finished = self.client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PGR_wh_in.Cin" + str(self.Id) + ".finish")
    
    def receivePieces(self, numPieces, piece):
        setValueCheck(self.enable, True, ua.VariantType.Boolean)
        setValueCheck(self.piece, piece, ua.VariantType.UInt16)
        setValueCheck(self.numPieces, numPieces, ua.VariantType.Int16)
        while self.finished.get_value() == False:
            pass
        setValueCheck(self.enable, False, ua.VariantType.Boolean)
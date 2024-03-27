import sys
sys.path.insert(0, "..")
from opcua import ua
from opcua import Client
from cin import Cin
from utils import setValueCheck



if __name__ == "__main__":
    client = Client("opc.tcp://127.0.0.1:4840")
    try:
        client.connect()

        cin1 = Cin(client, 1)
        cin1.get_nodes()
        cin1.receivePieces(2, 1)

        at1_out1 = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PRG_man.AT1_out1.enable")
        finish = client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.PLC_PRG_man.AT1_out1.finish")
        setValueCheck(at1_out1, True, ua.VariantType.Boolean)
        while finish.get_value() == False:
            pass
        setValueCheck(at1_out1, False, ua.VariantType.Boolean)
        


    except Exception as e:
        print(e)
    finally:
        client.disconnect()
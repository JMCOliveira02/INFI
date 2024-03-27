#include "wareHouseIn.hpp"
#include "database.h"
#include <vector>
#include <stdexcept>
#include <iostream>
#include <new>

int main(int argc, char *argv[])
{
    std::vector<order> orders;
    // order currOrder;

    UA_Client *client = UA_Client_new();
    UA_StatusCode retvalConnection, retvalRegisters;

    UA_ClientConfig_setDefault(UA_Client_getConfig(client));

    retvalConnection = UA_Client_connect(client, "opc.tcp://127.0.0.1:4840");
    if (retvalConnection != UA_STATUSCODE_GOOD)
    {
        fprintf(stderr, "Failed to connect to the server. Error code: %x\n", retvalConnection);
        UA_Client_delete(client);
        return EXIT_FAILURE;
    }

    char nodeIdRegisters[] = "|var|CODESYS Control Win V3 x64.Application.PLC_PGR_wh_in.Cin1.num_pieces";

    UA_Variant *valRegisters = UA_Variant_new();

    printf("\nReading the value of node (4, \"%s\"):\n", nodeIdRegisters);

    int i = 0;
    retvalRegisters = UA_Client_readValueAttribute(client, UA_NODEID_STRING(4, nodeIdRegisters), valRegisters);
    while (1)
    {
        if (i >= 4)
        {
            break;
        }
        printf("Enter the register to write: ");
        UA_UInt16 registerToWrite;
        std::cin >> registerToWrite;
        spawnPieces(client, i++, 1, 1);
    }

    UA_Variant_delete(valRegisters);

    UA_Client_disconnect(client);
    UA_Client_delete(client);

    return EXIT_SUCCESS;
    // Clean up
    /* CLOSE CONNECTION */
}
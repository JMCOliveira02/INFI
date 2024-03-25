/* #include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

void read_txt(const std::string &filename, std::vector<int> &type, std::vector<int> &quantity)
{
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line))
    {
        std::istringstream iss(line);
        int column1, column2;
        if (iss >> column1 >> column2)
        {
            type.push_back(column1);
            quantity.push_back(column2);
        }
    }
    file.close();
}

int main()
{
    std::vector<int> type;
    std::vector<int> quantity;
    read_txt("MES/db.txt", type, quantity);

    return 0;
}
 */

#include "open62541.h"
#include <stdexcept>
#include <iostream>
#include <new>

int main(int argc, char *argv[])
{
    UA_Client *client = UA_Client_new();
    UA_StatusCode retval, retvalRegisters, retvalOutputs, retvalInputs;

    UA_ClientConfig_setDefault(UA_Client_getConfig(client));

    retval = UA_Client_connect(client, "opc.tcp://127.0.0.1:4840");
    if (retval != UA_STATUSCODE_GOOD)
    {
        fprintf(stderr, "Failed to connect to the server. Error code: %x\n", retval);
        UA_Client_delete(client);
        return EXIT_FAILURE;
    }

    retvalRegisters = UA_Client_connect(client, "opc.tcp://127.0.0.1:4840");
    if (retvalRegisters != UA_STATUSCODE_GOOD)
    {
        fprintf(stderr, "Failed to connect to the server. Error code: %x\n", retvalRegisters);
        UA_Client_delete(client);
        return EXIT_FAILURE;
    }

    /* READ ATTRIBUTE REGISTERS*/

    char nodeIdRegisters[] = "|var|CODESYS Control Win V3 x64.Application.Variables.registers";
    printf("\nReading the value of node (4, \"%s\"):\n", nodeIdRegisters);
    UA_Variant *valRegisters = UA_Variant_new();
    retvalRegisters = UA_Client_readValueAttribute(client, UA_NODEID_STRING(4, nodeIdRegisters), valRegisters);
    if (retvalRegisters == UA_STATUSCODE_GOOD && UA_Variant_hasArrayType(valRegisters, &UA_TYPES[UA_TYPES_UINT16]))
    {
        UA_UInt16 *wordArrayRegisters = (UA_UInt16 *)valRegisters->data;
        for (size_t i = 0; i < valRegisters->arrayLength; i++)
        {
            printf("Element %zu is: %u\n", i, wordArrayRegisters[i]);
        }
        // Get user input for the new value
        UA_UInt16 newValueRegisters;
        printf("Enter the new value to write: ");
        if (scanf("%hu", &newValueRegisters) != 1)
        {
            fprintf(stderr, "Invalid input. Exiting...\n");
            UA_Variant_delete(valRegisters);
            UA_Client_disconnect(client);
            UA_Client_delete(client);
            return EXIT_FAILURE;
        }

        // Modify specific values in the array
        wordArrayRegisters[0] = newValueRegisters; // Change the value at index 0
        printf("\nWriting the modified array back to the server:\n");
        retvalRegisters = UA_Client_writeValueAttribute(client, UA_NODEID_STRING(4, nodeIdRegisters), valRegisters);
        if (retvalRegisters != UA_STATUSCODE_GOOD)
        {
            fprintf(stderr, "Failed to write the attribute. Error code: %x\n", retvalRegisters);
        }
    }
    else
    {
        fprintf(stderr, "Failed to read the attribute. Error code: %x\n", retvalRegisters);
    }

    UA_Variant_delete(valRegisters); // Don't forget to clean up

    /* READ ATTRIBUTE OUTPUTS*/

    char nodeIdOutputs[] = "|var|CODESYS Control Win V3 x64.Application.Variables.outputs";
    printf("\nReading the value of node (4, \"%s\"):\n", nodeIdOutputs);
    UA_Variant *valOutputs = UA_Variant_new();
    retvalOutputs = UA_Client_readValueAttribute(client, UA_NODEID_STRING(4, nodeIdOutputs), valOutputs);
    if (retvalOutputs == UA_STATUSCODE_GOOD && UA_Variant_hasArrayType(valOutputs, &UA_TYPES[UA_TYPES_BOOLEAN]))
    {
        UA_Boolean *boolArrayOutputs = (UA_Boolean *)valOutputs->data;
        for (size_t i = 0; i < valOutputs->arrayLength; i++)
        {
            printf("Element %zu is: %s\n", i, boolArrayOutputs[i] ? "true" : "false");
        }
        // Get user input for the new value
        UA_Boolean newValueOutputs;
        unsigned char tempOutputs;
        printf("Enter the new boolean value (0 for false, 1 for true): ");
        if (scanf("%hhu", &tempOutputs) != 1)
        {
            fprintf(stderr, "Invalid input. Exiting...\n");
            UA_Variant_delete(valOutputs);
            UA_Client_disconnect(client);
            UA_Client_delete(client);
            return EXIT_FAILURE;
        }
        newValueOutputs = (UA_Boolean)tempOutputs;

        // Modify specific values in the array
        boolArrayOutputs[0] = newValueOutputs; // Change the value at index 0
        printf("\nWriting the modified array back to the server:\n");
        retvalOutputs = UA_Client_writeValueAttribute(client, UA_NODEID_STRING(4, nodeIdOutputs), valOutputs);
        if (retvalOutputs != UA_STATUSCODE_GOOD)
        {
            fprintf(stderr, "Failed to write the attribute. Error code: %x\n", retvalOutputs);
        }
    }
    else
    {
        fprintf(stderr, "Failed to read the attribute. Error code: %x\n", retvalOutputs);
    }

    UA_Variant_delete(valOutputs); // Don't forget to clean up

    /* READ ATTRIBUTE INPUTS*/

    char nodeIdInputs[] = "|var|CODESYS Control Win V3 x64.Application.Variables.inputs";
    printf("\nReading the value of node (4, \"%s\"):\n", nodeIdInputs);
    UA_Variant *valInputs = UA_Variant_new();
    retvalInputs = UA_Client_readValueAttribute(client, UA_NODEID_STRING(4, nodeIdInputs), valInputs);
    if (retvalInputs == UA_STATUSCODE_GOOD && UA_Variant_hasArrayType(valInputs, &UA_TYPES[UA_TYPES_BOOLEAN]))
    {
        UA_Boolean *boolArrayInputs = (UA_Boolean *)valInputs->data;
        for (size_t i = 0; i < valInputs->arrayLength; i++)
        {
            printf("Element %zu is: %s\n", i, boolArrayInputs[i] ? "true" : "false");
        }
    }
    else
    {
        fprintf(stderr, "Failed to read the attribute. Error code: %x\n", retvalInputs);
    }

    UA_Variant_delete(valInputs); // Don't forget to clean up

    return 0;

    /* CLOSE CONNECTION */

    UA_Client_disconnect(client);
    UA_Client_delete(client);

    return EXIT_SUCCESS;
}
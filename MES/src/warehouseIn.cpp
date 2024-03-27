#include "../include/warehouseIn.hpp"

int spawnPieces(UA_Client *client, int conveyorId, int pieceType, int numPieces)
{
    std::string nodeConveyorID = "|var|CODESYS Control Win V3 x64.Application.PLC_PGR_wh_in.Cin";
    nodeConveyorID += std::to_string(conveyorId);
    nodeConveyorID += ".";
    std::string nodePieceType = nodeConveyorID + "piece";
    std::string nodeNumPieces = nodeConveyorID + "numPieces";

    UA_Variant *varPieceType = UA_Variant_new();
    UA_Variant *varPieceQuantity = UA_Variant_new();
    UA_Variant *varEnable = UA_Variant_new();
    UA_Int16 UApieceType = pieceType;
    UA_Int16 UAnumPieces = numPieces;

    // Update the type and quantity of pieces to be spawned
    UA_Variant_setScalarCopy(varPieceType, &UApieceType, &UA_TYPES[UA_TYPES_INT16]);
    UA_Variant_setScalarCopy(varPieceQuantity, &UAnumPieces, &UA_TYPES[UA_TYPES_INT16]);

    char *aux = new char[nodePieceType.length() + 1]; // +1 for null terminator
    std::strcpy(aux, nodePieceType.c_str());
    UA_Client_writeValueAttribute(client, UA_NODEID_STRING(4, aux), varPieceType);
    UA_Client_writeValueAttribute(client, UA_NODEID_STRING(4, aux), varPieceQuantity);

    // Enable the spawning of pieces
    UA_Variant_setScalarCopy(varEnable, &conveyorId, &UA_TYPES[UA_TYPES_INT32]);
    UA_Client_writeValueAttribute(client, UA_NODEID_STRING(4, aux), varEnable);

    return 0;
}
#include <iostream>
#include <string>
#include "open62541.h"
/*
    Spawns pieces of a given entrance conveyor belt
 */
int spawnPieces(UA_Client *client, int conveyorId, int pieceType, int numPieces);

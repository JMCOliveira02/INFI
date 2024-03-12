#include "tinyxml2.h"
#include <iostream>

/* Data structure to store relevant socket variables
    @param clientName: name of the client
    @param orderNumber: order number
    @param workPiece: work piece name
    @param quantity: quantity of work pieces
    @param dueDate: due date of the order
    @param latePenalty: penalty for late delivery
    @param earlyPenalty: penalty for early delivery
 */
typedef struct
{
    std::string clientName;
    int orderNumber;
    std::string workPiece;
    int quantity;
    int dueDate;
    float latePenalty;
    float earlyPenalty;
} parsedOrder;

/* Parse the received XML data
    @param message: received XML data
    @return parsedOrder structure with the parsed data
 */
parsedOrder parseOrder(char *message);

/* Print the parsed order data
    @param orderData: parsedOrder structure with the parsed data
 */
void printOrder(parsedOrder orderData);

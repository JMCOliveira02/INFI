#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

/* structure representing a single order
    @param type
        type of piece
    @param quantity
        quantity of pieces
    @param dueDate
        due date of the order
    @param status
        0 - ordered;
        1 - arriving;
        2 - arrived;
        3 - in production;
        4 - finished;
*/
typedef struct
{
    int type;
    int quantity;
    int dueDate;
    int status;
} order;

/*
    Reads the database file and stores the orders in a vector
    @param filename
        name of the file to be read
    @param orders
        vector to store the orders
 */
void read_database(const std::string &filename, std::vector<order> &orders);

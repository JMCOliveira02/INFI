#include "../include/database.h"

void read_database(const std::string &filename, std::vector<order> &orders)
{
    order order_aux;
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line))
    {
        std::istringstream iss(line);
        int column1, column2, column3, column4;
        if (iss >> column1 >> column2 >> column3 >> column4)
        {
            order_aux.type = column1;
            order_aux.quantity = column2;
            order_aux.dueDate = column3;
            order_aux.status = column4;
            orders.push_back(order_aux);
        }
    }
    file.close();
}

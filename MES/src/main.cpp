#include <iostream>
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

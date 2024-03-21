#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

typedef struct
{
    std::string clientName;
    int orderNumber;
    std::string workPiece;
    int quantity;
    int dueDate;
    float latePenalty;
    float earlyPenalty;
} Order;

std::vector<Order> readDatabase(const std::string &filename)
{
    std::vector<Order> records;
}
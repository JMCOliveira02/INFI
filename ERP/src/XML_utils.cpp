#include "XML_utils.hpp"

parsedOrder parseOrder(char *message)
{

    // Create the XML document for the received data
    tinyxml2::XMLDocument doc;
    tinyxml2::XMLElement *root, *client, *order;

    // Check if the XML data was parsed
    if (doc.Parse(message) != tinyxml2::XML_SUCCESS)
    {
        std::cerr << "Error parsing XML data." << std::endl;
        throw std::runtime_error("Error parsing XML data.");
    }

    // Get the root element of the XML document
    root = doc.RootElement();
    if (!root)
    {
        std::cerr << "Error: Root element not found." << std::endl;
        throw std::runtime_error("Error: Root element not found.");
    }

    // Get the client element
    client = root->FirstChildElement("Client");
    if (client)
    {
        const char *name = client->Attribute("NameId");
    }

    // Get the order element
    order = root->FirstChildElement("Order");

    // Create a parsedOrder structure to store the parsed data
    parsedOrder orderData;

    // Assign the parsed data to the parsedOrder structure
    if (order)
    {

        orderData.clientName = client->Attribute("NameId");
        orderData.orderNumber = std::atoi(order->Attribute("Number"));
        orderData.workPiece = order->Attribute("WorkPiece");
        order->QueryIntAttribute("Quantity", &orderData.quantity);
        order->QueryIntAttribute("DueDate", &orderData.dueDate);
        order->QueryFloatAttribute("LatePen", &orderData.latePenalty);
        order->QueryFloatAttribute("EarlyPen", &orderData.earlyPenalty);
    }

    return orderData;
}

void printOrder(parsedOrder orderData)
{
    std::cout << "Client: " << orderData.clientName << std::endl;
    std::cout << "Order Number: " << orderData.orderNumber << std::endl;
    std::cout << "Work Piece: " << orderData.workPiece << std::endl;
    std::cout << "Quantity: " << orderData.quantity << std::endl;
    std::cout << "Due Date: " << orderData.dueDate << std::endl;
    std::cout << "Late Penalty: " << orderData.latePenalty << std::endl;
    std::cout << "Early Penalty: " << orderData.earlyPenalty << std::endl;
}

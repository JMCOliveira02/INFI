#include <iostream>
#include <vector>
#include "UDP_comms.hpp"
#include "XML_utils.hpp"
#include "tinyxml2.h"

#pragma comment(lib, "Ws2_32.lib")

int main()
{
    // Setup communications
    socketInfo *udpSocket;
    udpSocket = new socketInfo;

    // Create a orderData structure to store the parsed data
    std::vector<parsedOrder> orderData;

    if (initializeSocket(udpSocket) < 0)
    {
        return -1;
    }

    while (1)
    {
        // Receive data from the socket
        if (receiveData(udpSocket) < 0)
        {
            return -1;
        }

        // Parse the data
        try
        {
            orderData.push_back(parseOrder(udpSocket->buffer));
        }
        catch (const std::runtime_error &e)
        {
            std::cout << "Caught an exception: " << e.what() << std::endl;
            return -1;
        }

        // Store the data in the database
        }
}

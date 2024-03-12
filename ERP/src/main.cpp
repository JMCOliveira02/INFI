#include <iostream>
#include <vector>
#include "UDP_comms.hpp"
#include "XML_utils.hpp"
#include "tinyxml2.h"

#pragma comment(lib, "Ws2_32.lib")

int main()
{
    bool debug = true;
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
        if (debug)
            std::cout << "Waiting for data..." << std::endl;

        // Receive data from the client
        if (receiveData(udpSocket) < 0)
        {
            if (debug)
                std::cerr << "Error receiving data." << std::endl;
            return -1;
        }

        if (debug)
            std::cout << "Received data: " << udpSocket->buffer << std::endl;

        // Parse the received data
        try
        {
            orderData.push_back(parseOrder(udpSocket->buffer));
        }
        catch (const std::runtime_error &e)
        {
            std::cout << "Caught an exception: " << e.what() << std::endl;
            return -1;
        }

        // printOrder(orderData.back());
    }
}

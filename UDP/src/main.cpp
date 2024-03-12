#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <WS2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")

#define PORT 12345 // Change this to your desired port

std::string readFromFile(const std::string &filename)
{
    std::ifstream file(filename);
    std::string content;
    if (file.is_open())
    {
        std::string line;
        while (std::getline(file, line))
        {
            content += line;
        }
        file.close();
    }
    return content;
}

int main()
{
    WSADATA wsaData;
    int iResult;

    // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0)
    {
        std::cerr << "WSAStartup failed: " << iResult << std::endl;
        return 1;
    }

    SOCKET sock;
    struct sockaddr_in server_addr;
    std::ostringstream filename;
    std::string message;

    // Create UDP socket
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET)
    {
        std::cerr << "Error creating socket: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return 1;
    }

    // Set up server address and port
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr); // Change this to your server's IP address

    // Send the message
    int fileNumber = 1;
    char fileChar = 'a';
    while (1)
    {
        std::cin.get();
        filename << "C:/Users/jmc_o/Documents/A4_S2/INFI/code/Sample_orders/command"
                 << fileNumber++
                 << ".xml";

        std::cout << "Reading file: " << filename.str() << std::endl;
        message = readFromFile(filename.str());
        if (message.empty())
        {
            std::cout << "File not found: " << filename.str() << std::endl;
            // Clear the stringstream and string
            filename.str("");
            message.clear();

            filename << "C:/Users/jmc_o/Documents/A4_S2/INFI/code/Sample_orders/command"
                     << --fileNumber
                     << fileChar++
                     << ".xml";

            std::cout << "Reading file: " << filename.str() << std::endl;
            message = readFromFile(filename.str());
            if (message.empty())
            {
                // Clear the stringstream and string
                filename.str("");
                message.clear();
                fileChar = 'a';
                fileNumber++;
                continue;
            }
        }

        std::cout << "Sending message: " << std::endl
                  << message << std::endl;

        iResult = sendto(sock, message.c_str(), message.length(), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (iResult == SOCKET_ERROR)
        {
            std::cerr << "Error sending message: " << WSAGetLastError() << std::endl;
            closesocket(sock);
            WSACleanup();
            return 1;
        }

        // Clear the stringstream and string
        filename.str("");
        message.clear();
    }

    // Close the socket
    closesocket(sock);
    WSACleanup();

    return 0;
}

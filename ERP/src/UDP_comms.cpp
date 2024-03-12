#include "UDP_comms.hpp"

int initializeSocket(socketInfo *udpSocket)
{
    // Initialize Winsock
    udpSocket->iResult = WSAStartup(MAKEWORD(2, 2), &udpSocket->wsaData);
    // Check for errors
    if (udpSocket->iResult != 0)
    {
        std::cerr << "WSAStartup failed: " << udpSocket->iResult << std::endl;
        return -1;
    }

    // Create UDP socket
    udpSocket->sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    // Check for errors
    if (udpSocket->sock == INVALID_SOCKET)
    {
        std::cerr << "Error creating socket: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return -2;
    }

    // Assign port number
    udpSocket->port = DEFAULT_PORT;
    // Bind the socket to the port
    udpSocket->server_addr.sin_family = AF_INET;
    udpSocket->server_addr.sin_port = htons(udpSocket->port);
    udpSocket->server_addr.sin_addr.s_addr = INADDR_ANY;

    // Check for errors
    if (bind(udpSocket->sock, (struct sockaddr *)&(udpSocket->server_addr), sizeof(udpSocket->server_addr)) == SOCKET_ERROR)
    {
        std::cerr << "Bind failed with error: " << WSAGetLastError() << std::endl;
        closesocket(udpSocket->sock);
        WSACleanup();
        return -3;
    }

    return 1;
}

int receiveData(socketInfo *udpSocket)
{
    int recv_len;
    if ((recv_len = recvfrom(udpSocket->sock, udpSocket->buffer, sizeof(udpSocket->buffer), 0, NULL, NULL)) == SOCKET_ERROR)
    {
        std::cerr << "Receive failed with error: " << WSAGetLastError() << std::endl;
        closesocket(udpSocket->sock);
        WSACleanup();
        return -1;
    }
    // Null-terminate the received data to use with tinyxml2
    udpSocket->buffer[recv_len] = '\0';

    return 1;
}
#include <WS2tcpip.h>
#include <iostream>

#define DEFAULT_PORT 12345
#define DEFAULT_BUFLEN 1024

/* Data structure to store relevant socket variables
    @param wsaData: Winsock data
    @param iResult: result of Winsock operations
    @param sock: socket data structure
    @param server_addr: server address
    @param port: port number
    @param buffer: buffer to store received data
    @param recv_len: length of received data
 */
typedef struct
{
    WSADATA wsaData;
    int iResult;
    SOCKET sock;
    struct sockaddr_in server_addr;
    int port;
    char buffer[DEFAULT_BUFLEN];
    int recv_len;
} socketInfo;

/* Initialize the socket data structure with
predefined values
    @param udpSocket: pointer to the socketInfo structure
    @returns -1 if error, 1 if not*/
int initializeSocket(socketInfo *udpSocket);

/* Receive data from the client
    @param udpSocket: pointer to the socketInfo structure
    @returns -1 if error, 1 if not
    */
int receiveData(socketInfo *udpSocket);

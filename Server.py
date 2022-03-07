from socket import *

localIP = "192.168.0.180"
localPort = 12000
bufferSize = 2048

serverSocket = socket(AF_INET,SOCK_DGRAM)

serverSocket.bind((localIP, localPort))

print ('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
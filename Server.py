from socket import *

localIP = "196.42.83.200" # insert own network IP
localPort = 24000
bufferSize = 2048

serverSocket = socket(AF_INET,SOCK_DGRAM)

serverSocket.bind((localIP, localPort))

print ('Server is Up')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
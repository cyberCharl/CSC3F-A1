from socket import *
import zlib

localIP = "192.168.0.180" # insert own network IP
localPort = 12000
bufferSize = 2048

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((localIP, localPort))

def checkHash(message, recievedHash):
    return (zlib.adler32(message.encode()) == int(recievedHash))

# server active confirmation
print ('Server is Up')

# listening for messages + parsing protocol messages
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    packetRecv = message.decode()

    # get <clientName> from packet recieved
    clientName = packetRecv[packetRecv.find('<')+1:packetRecv.find('>')]
    
    # get [hashKey] from packet
    hashKey = packetRecv[packetRecv.find('[')+1:packetRecv.find(']')]
    # get {message} from packet recieved
    messageContent = packetRecv[packetRecv.find('{')+1:packetRecv.find('}')]

    # message confirmation via hash and print
    if checkHash(messageContent, hashKey):
        serverSocket.sendto("msgRcvd".encode(), clientAddress)
        print(clientName + '>> ' + messageContent)
    else: 
        serverSocket.sendto("msgLost".encode(), clientAddress)
    

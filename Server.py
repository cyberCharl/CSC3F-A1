from socket import *
import zlib

homeIP = "192.168.0.180" # insert own network IP
uctIP = "196.42.86.45"
localPort = 24000
bufferSize = 2048

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((homeIP, localPort))

def checkHash(message, recievedHash):
    return (zlib.adler32(message.encode()) == int(recievedHash))

def msgProtocol(packet):
    
    # get <T>type</T>
    msgType = packet[packet.find("<T>")+3:packet.find("</T>")]
    
    # get <ID>clientName</ID> from packet recieved
    clientName = packet[packet.find('<ID>')+4:packet.find('</ID>')]
    
    # get [hashKey] from packet
    hashKey = packet[packet.find("<hK>")+4:packet.find('</hK>')]
    
    return [msgType, clientName, hashKey]

# server active confirmation
print ('Server is Up')

# listening for messages + parsing protocol messages
while True:
    message, clientAddress = serverSocket.recvfrom(2048)

    packetRecv = message.decode()
    msgRcv = msgProtocol(packetRecv)
    
    if msgRcv[0] == "quit":
        messageContent = msgRcv[1] + " disconnected --- removing messages sent"
        print(messageContent) # send to other clients on server - seperate thread
        break # remove client that quit from clientArray
    
    # get {message} from packet recieved
    messageContent = packetRecv[packetRecv.find('{')+1:packetRecv.find('}')]

    # message confirmation via hash and print
    if checkHash(messageContent, msgRcv[2]):
        serverSocket.sendto("msgRcvd".encode(), clientAddress)
        print(msgRcv[1] + '>> ' + messageContent) # send to other clients - thread
    else: 
        serverSocket.sendto("msgLost".encode(), clientAddress) # wait for response - thread?

from socket import *
import zlib

homeIP = "192.168.0.180" # insert own network IP
uctIP = "196.42.86.45"
uctIP1 = "196.42.81.129"
localPort = 24000
bufferSize = 2048
clientArray = []

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((homeIP, localPort))

class client():
    def __init__(identifier, ipAddress, portAddress, encryptionKey):
        clientID = identifier
        clientAddress = [ipAddress, portAddress]
        clientKey = encryptionKey

def checkHash(message, recievedHash):
    return (zlib.adler32(message.encode()) == int(recievedHash))

# parsing protocol header add counter
def msgProtocol(packet):
    packet = packet.decode()

    # get <T>type</T>
    msgType = packet[packet.find("<T>")+3:packet.find("</T>")]
    
    # get <ID>clientName</ID> from packet recieved
    clientName = packet[packet.find('<ID>')+4:packet.find('</ID>')]
    
    # get [hashKey] from packet
    hashKey = packet[packet.find("<hK>")+4:packet.find('</hK>')]
    
    # message confirmation via hash
    if checkHash(packet[:packet.find("<hK>")], hashKey):
        # send message AK
        serverSocket.sendto("msgRcvd".encode(), currentClientAdd)
    else: 
        serverSocket.sendto("msgLost".encode(), currentClientAdd) 
        # wait for response - thread?
    
    if (msgType == "touch"):
        encKey = packet[packet.find("<ek>") + 4: packet.find("</ek>")]
        return [msgType, clientName, encKey]

    # get sent message and decrypt (would need clientID)
    msgContent = decryptMessage(packet)

    return [msgType, clientName, msgContent]

# to take package and remove message and decrypt it
def decryptMessage(msgCont):
    return msgCont[msgCont.find("<msg>")+5:msgCont.find("</msg>")]

# broadcast message sent to all other "connected" clients - use clientArray
def broadcast(clients):    
    print("hi")
    # do stuff on seperate threads 

# server active confirmation
print ('Server is Up on: ' + homeIP)

# start thread listen for touch and make global array of clients

# listening for messages on seperate thread 
while True:
    packetRecv, currentClientAdd = serverSocket.recvfrom(2048)

    msgRcv = msgProtocol(packetRecv)
    
    if msgRcv[0] == "touch":
        clientArray.append(client(msgRcv[1], currentClientAdd, msgRcv[2]))
        print(msgRcv[1] + " connected") # broadcast to everyone else
    
    if msgRcv[0] == "quit":
        messageContent = msgRcv[1] + " disconnected --- removing messages sent"
        print(messageContent) # send to other clients on server - 
        break # remove client that quit from clientArray
    
    if msgRcv[0] == "msg":
        messageContent = msgRcv[2]
        print(msgRcv[1] + '>> ' + messageContent)

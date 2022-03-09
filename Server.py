from socket import *
import zlib
import threading as thr
import time

homeIP = "192.168.0.180" # insert own network IP
uctIP = "196.42.86.45"
uctIP1 = "196.42.81.129"
localPort = 24000
bufferSize = 2048
clientArray = []

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((homeIP, localPort))


class listenThread(thr.Thread):
    def __init__(self, threadID):
        thr.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        listen()

class client():
    def __init__(identifier, ipAddress, portAddress, encryptionKey):
        clientID = identifier
        clientAddress = [ipAddress, portAddress]
        clientKey = encryptionKey


def encryptMessage(message, key):
    keycount = 0
    output = ''

    for i in message:
        icode = ord(i) + key[keycount]
        
        if icode > 126:
            icode = (icode - 126) + 31
        
        keycount = keycount + 1
        if keycount == 5:
            keycount = 0

        output = output + chr(icode)

    return "<msg>" + output + "</msg>"
# to take package and remove message and decrypt it

def decryptMessage(message, key):
    msg = message[message.find("<msg>")+5:message.find("</msg>")]
    keycount = 0
    output = ''

    for i in msg:
        icode = ord(i) - key[keycount]
        
        if icode < 32:
            icode = (icode + 126) - 31
        
        keycount = keycount + 1
        if keycount == 5:
            keycount = 0

        output = output + chr(icode)
    
    return output

def msgPacket(name, num, messageContent): # client side order and reorder
    msgType = "<T>msg</T>"
    clientName = '<ID>' + name + '</ID>'
    clientNum = "<n>" + str(clientNum) + "</n>"
    msgCrypt = encryptMessage(messageContent, clientArrray[num].encryptionKey)
    packet = msgType + clientName + clientNum + msgCrypt
    msgHash = hash(packet)
    return packet + msgHash

# listen method for thread
def listen():
    while True:
        packetRecv, currentClientAdd = serverSocket.recvfrom(2048)

        msgRcv = msgProtocol(packetRecv, currentClientAdd)
    
        if msgRcv[0] == "touch":
            clientArray.append(client(msgRcv[1], currentClientAdd, msgRcv[2]))
            clientPos = len(clientArray) - 1
            msgPacket(clientArray[clientPos].identifier, clientPos, messageContent)

            # msgPacket(currentClientAdd, messageContent)
            print(msgRcv[1] + " connected") # broadcast to everyone else
    
        if msgRcv[0] == "quit":
            messageContent = msgRcv[1] + " disconnected --- removing messages sent"
            print(messageContent) # send to other clients on server - 
            break # remove client that quit from clientArray
    
        if msgRcv[0] == "msg":
            messageContent = msgRcv[2]
            print(msgRcv[1] + '>> ' + messageContent)

def checkHash(message, recievedHash):
    return (zlib.adler32(message.encode()) == int(recievedHash))

# parsing protocol header add counter
def msgProtocol(packet, clientAdd):
    packet = packet.decode()

    # get <T>type</T>
    msgType = packet[packet.find("<T>")+3:packet.find("</T>")]
    
    # get <ID>clientName</ID> from packet recieved
    clientName = packet[packet.find('<ID>')+4:packet.find('</ID>')]
    
    # get [hashKey] from packet
    hashKey = packet[packet.find("<hK>")+4:packet.find('</hK>')]
    
    clientNum = packet[packet.find("<n>")+3:packet.find("</n>")]

    # message confirmation via hash
    if checkHash(packet[:packet.find("<hK>")], hashKey):
        # send message AK
        serverSocket.sendto("msgRcvd".encode(), clientAdd)
    else: 
        serverSocket.sendto("msgLost".encode(), clientAdd) 
        # wait for response - thread?
    
    if (msgType == "touch"):
        encKey = packet[packet.find("<ek>") + 4: packet.find("</ek>")]
        return [msgType, clientName, encKey]

    # get sent message and decrypt (would need clientID)
    msgContent = decryptMessage(packet, clientArray[int(clientNum)].encryptionKey)

    return [msgType, clientName, msgContent]


# broadcast message sent to all other "connected" clients - use clientArray
def broadcast(packet, sendingClient):
    for i in clientArray:
        if i != sendingClient:
            clientSocket.sendto(packet.encode(), i.clientAddress)
    
    # timeout functionality
        tic = time.perf_counter()
    
        while(time.perf_counter() - tic <= 0.5):
            msgACK, serverAddress = clientSocket.recvfrom(2048)
        
            if(msgACK.decode() == "msgLost"):
                tic = time.perf_counter()
                clientSocket.sendto(packet.encode(), serverDetails)
            else:
                break        

    # do stuff on seperate threads 

def main():
# server active confirmation
    print ('Server is Up on: ' + homeIP)

    thread1 = listenThread(1)
    thread1.start()

if __name__ == "__main__":
    main()

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

class client:
    def __init__(self, clientID, ipAddress, portAddress, encryptionKey):
        self.clientID = clientID
        self.ipAddress= ipAddress
        self.portAddress = portAddress
        self.encryptionKey = encryptionKey

class listenThread(thr.Thread):
    def __init__(self, threadID):
        thr.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        listen()

# listen method for thread
def listen():
    while True:
        packetRecv, currentClientAdd = serverSocket.recvfrom(2048)
        msgRcv = msgProtocol(packetRecv, currentClientAdd)

        for i in clientArray:
            if i.ipAddress == currentClientAdd[0] and i.portAddress == currentClientAdd[1]:
                sendClient = i 

        if msgRcv[0] == "touch":
            encKey = [0,0,0,0,0]
            key = msgRcv[2]
            i = 0
            while i<= 9:
                encKey[i//2] = int(key[i:i+2])
                i+= 2
            newCli = client(clientID= msgRcv[1], 
            ipAddress= currentClientAdd[0], 
            portAddress= currentClientAdd[1], 
            encryptionKey= encKey)
            clientArray.append(newCli)
            
            print(msgRcv[1] + " connected") # broadcast to everyone else
    
        if msgRcv[0] == "quit":
            messageContent = msgRcv[1] + " disconnected --- removing messages sent"
            print(messageContent) # send to other clients on server - 
            break # remove client that quit from clientArray
    
        if msgRcv[0] == "msg":
            # messageContent = decryptMessage(msgRcv[2], key)
            broadcast(msgRcv[2], sendClient)



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

    return "<cnt>" + output + "</cnt>"
# to take package and remove message and decrypt it

def decryptMessage(message, key):
    keycount = 0
    output = ''

    for i in message:
        icode = ord(i) - key[keycount]
        
        if icode < 32:
            icode = (icode + 126) - 31
        
        keycount = keycount + 1
        if keycount == 5:
            keycount = 0

        output = output + chr(icode)
    
    return output

# command header (not normal message)
def commandHeader(command, name):
    msgType = "<T>"+ command + "</T>"
    clientName = '<ID>' + name + '</ID>'
    return msgType + clientName

def msgPacket(name, messageContent): 
    msgType = "<T>msg</T>"
    clientName = '<ID>' + name + '</ID>'
    packet = msgType + clientName + messageContent
    msgHash = hash(packet)
    return packet + msgHash

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

    for i in clientArray:
        key = []
        if i.ipAddress == clientAdd[0] and i.portAddress == clientAdd[1]:
            key = i.encryptionKey
    
    msg = packet[packet.find("<cnt>") + 10 :packet.find("</cnt>")]
    msgContent = decryptMessage(msg, key)

    return [msgType, clientName, msgContent]

def hash(message):
    return "<hK>" + str(zlib.adler32(message.encode())) + "</hK>"

# broadcast message sent to all other "connected" clients - use clientArray
def broadcast(packet, sendingClient):

    for i in clientArray:
        if i == sendingClient:
            msgCrypt = str(encryptMessage(packet, i.encryptionKey))
            package = msgPacket(sendingClient.clientID, msgCrypt)
            clientAddress = (i.ipAddress, i.portAddress)
            serverSocket.sendto(package.encode(), clientAddress)
    
         # timeout functionality
            tic = time.perf_counter()
    
            while(time.perf_counter() - tic <= 0.5):
                msgACK, serverAddress = serverSocket.recvfrom(2048)
        
                if(msgACK.decode() == "msgLost"):
                    tic = time.perf_counter()
                    serverSocket.sendto(package.encode(), clientAddress)
                else:
                    continue        

    # do stuff on seperate threads 

def main():
# server active confirmation
    print ('Server is Up on: ' + homeIP)

    thread1 = listenThread(1)
    thread1.start()

if __name__ == "__main__":
    main()

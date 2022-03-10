from socket import *
import zlib
import threading as thr
import time

homeIP = "192.168.0.134" # insert own network IP
uctIP = "196.42.86.45"
uctIP1 = "196.42.81.129"
localPort = 24000
bufferSize = 2048
clientArray = []

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((homeIP, localPort))

prevMessage = ""

def main():
# server active confirmation
    print ('Server is Up on: ' + homeIP)

    thread1 = listenThread(1)
    thread1.start()

    serverDown()

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
            leave(sendClient)
    
        if msgRcv[0] == "msg":
            broadcast(msgRcv[2], sendClient)

def serverDown():
    broadcastAll(commandHeader("serverDown", "server"))

def leave(sendClient):
    messageContent = msgRcv[1] + " disconnected --- removing messages sent"
    packet = commandHeader("leave", msgRcv[1]) + "<cnt>" + messageContent + "</cnt>"
    hashKey = hash(packet)
    sendMsg = packet + hashKey        
    broadcast(sendMsg, sendClient)

def msgACK(status, clientDisplayName):
    sendMsg = commandHeader("ack", clientDisplayName)
    sendMsg += "<st>" + status + "</st>"
    haskey = hash(sendMsg)
    return sendMsg + haskey

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
    
    # get <hK>hashKey</hK> from packet
    hashKey = packet[packet.find("<hK>")+4:packet.find('</hK>')]

    # message confirmation via hash
    if checkHash(packet[:packet.find("<hK>")], hashKey):
        # send message Ackowledgement
        status = "msgRcvd"
        serverSocket.sendto(msgACK(status, clientName).encode(), clientAdd)
    else: 
        status = "msgLost"
        serverSocket.sendto(msgACK(status, clientName).encode(), clientAdd) 
        # wait for response - thread?
    
    # if touch, get encryption key
    if (msgType == "touch"):
        encKey = packet[packet.find("<ek>") + 4: packet.find("</ek>")]
        return [msgType, clientName, encKey]
    
    # if ackowledge message, return type, clientDisplayName, status,
    if msgType == "ack":
            ackStatus = packet[packet.find("<st>")+4:packet.find("</st>")]
            return [msgType, clientName, ackStatus]
    
    for i in clientArray:
        key = []
        if i.ipAddress == clientAdd[0] and i.portAddress == clientAdd[1]:
            key = i.encryptionKey
    
    msg = packet[packet.find("<cnt>") +  5:packet.find("</cnt>")]
    msgContent = decryptMessage(msg, key)

    return [msgType, clientName, msgContent]

def hash(message):
    return "<hK>" + str(zlib.adler32(message.encode())) + "</hK>"

# broadcast message sent to all other "connected" clients - use clientArray
def broadcastAll(packet): 
    for i in clientArray:
        package = str(encryptMessage(packet, i.encryptionKey))
        clientAddress = (i.ipAddress, i.portAddress)
        serverSocket.sendto(package.encode(), clientAddress)

def broadcast(packet, sendingClient):

    for i in clientArray:
        if i != sendingClient:
            msgCrypt = str(encryptMessage(packet, i.encryptionKey))
            package = msgPacket(sendingClient.clientID, msgCrypt)
            clientAddress = (i.ipAddress, i.portAddress)
            serverSocket.sendto(package.encode(), clientAddress)

if __name__ == "__main__":
    main()

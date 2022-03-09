from socket import*
import threading as thr
import zlib
import time

# Network stuff
homeIP = "192.168.0.180"
uctIP = "196.42.81.129"

# connect to room >> enter IP
# serverIP = input("enter server IP ")
serverInfo = (homeIP, 24000) # insert own network IP

clientSocket = socket(AF_INET, SOCK_DGRAM)
count = 0
encryptKey = "12345000"
clientID = 'DieKwaaiRatel'
clientNum = 0
#clientID = input('Enter identifier:')


# Send and confirm thread to take messages passed to it, send to server and wait for response. 
class recieveThread(thr.Thread):
    def __init__(self, threadID,name,package,servInf):
        thr.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.package = package
        self.servInf = servInf
    
    def run(self):
        while(True):
            recieveMessage()
def recieveMessage():
     while True:
        recievedMessage, serverAddress = serverSocket.recvfrom(2048)
        # packetRecv, currentClientAdd = serverSocket.recvfrom(2048)

        msgRcv = msgProtocol(packetRecv, currentClientAdd)
    
        if msgRcv[0] == "touch":
            clientArray.append(client(msgRcv[1], currentClientAdd, msgRcv[2]))
            # msgPacket(currentClientAdd, messageContent)
            print(msgRcv[1] + " connected") # broadcast to everyone else
    
        if msgRcv[0] == "quit":
            messageContent = msgRcv[1] + " disconnected --- removing messages sent"
            print(messageContent) # send to other clients on server - 
            break # remove client that quit from clientArray
    
        if msgRcv[0] == "msg":
            messageContent = msgRcv[2]
            print(msgRcv[1] + '>> ' + messageContent)
    
    

class sendThread(thr.Thread):
    def __init__(self, threadID, name, package, servInf):
        thr.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.package = package
        self.servInf = servInf

    def run(self):
        sendMessage(self.package, self.servInf)
        
# send and check message
def sendMessage(packet, serverDetails):
    clientSocket.sendto(packet.encode(), serverDetails)
    
    # timeout functionality
    tic = time.perf_counter()
    
    while(time.perf_counter() - tic <= 0.5):
        msgACK, serverAddress = clientSocket.recvfrom(2048)
        
        if(msgACK.decode() == "msgLost"):
            tic = time.perf_counter()
            clientSocket.sendto(packet.encode(), serverDetails)
        else:
             break        

# hash function
def hash(message):
    return "<hK>" + str(zlib.adler32(message.encode())) + "</hK>"

# command header (not normal message)
def commandHeader(command, name):
    msgType = "<T>"+ command + "</T>"
    clientName = '<ID>' + name + '</ID>'
    return msgType + clientName

# build the message packet with header and message
def msgPacket(name, messageContent): # client side order and reorder
    msgType = "<T>msg</T>"
    clientName = '<ID>' + name + '</ID>'
    packet = msgType + clientName + "<msg>" + messageContent + "</msg>"
    msgHash = hash(packet)
    return packet + msgHash

#quit function
def quit():
    sendMsg = commandHeader("quit", clientID)
    hashKey = hash(sendMsg)
    sendMsg += hashKey
    sendMessage(sendMsg, serverInfo)
    #  clientSocket.sendto(sendMsg.encode(),serverInfo)
    clientSocket.close()

def touch(name, encryptKey):
    encKey = "<ek>" + encryptKey + "</ek>"
    sendMsg = commandHeader("touch", name) + encKey
    hashKey = hash(sendMsg)
    sendMsg += hashKey
    # clientSocket.sendto(sendMsg.encode(), serverDetails)
    sendMessage(sendMsg, serverInfo)

# parsing protocol header add counter
def msgProtocol(packet, serverAddress):
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
        serverSocket.sendto("msgRcvd".encode(), serverAddress)
    else: 
        serverSocket.sendto("msgLost".encode(), serverAddress) 
        # wait for response - thread?
    
    if (msgType == "touch"):
        encKey = packet[packet.find("<ek>") + 4: packet.find("</ek>")]
        return [msgType, clientName, encKey]

    # get sent message and decrypt (would need clientID)
    msgContent = decryptMessage(packet)

    return [msgType, clientName, msgContent]

# touch server 
touch(clientID, encryptKey)

message = ''
while(True):
    message = input('msg > ')

    # if command 
    if(message[0] == '/'):
        if(message == '/quit'):
            quit()
            break # neccassary? 
    
    thread1 = sendThread(1, "Thread-1", msgPacket(clientID, message), serverInfo)
    thread1.start()

    # client side integrity check after broadcast
    
# new thread to listen for messages from server only if server touched.
        
clientSocket.close()

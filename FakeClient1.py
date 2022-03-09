from socket import*
import threading as thr
import zlib
import time

# Network stuff
homeIP = "192.168.0.180"
uctIP = "196.42.81.129"

# connect to room >> enter IP
# serverIP = input("enter server IP ")
serverInfo = (uctIP, 24000) # insert own network IP

clientSocket = socket(AF_INET, SOCK_DGRAM)
count = 0
key = "12345"
clientID = 'DieKwaaiRatel'
# clientName = input('Enter identifier:')


# Send and confirm thread to take messages passed to it, send to server and wait for response. 
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
    
    while(time.perf_counter() - tic <= 0.0000004):
        print(time.perf_counter() - tic)
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

# touch server 
touch(clientID, key)

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

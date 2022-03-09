from socket import*
import threading as thr
import zlib

# Network stuff
homeIP = "192.168.0.180"
uctIP = "196.42.86.45"
serverInfo = (homeIP, 24000) # insert own network IP
clientSocket = socket(AF_INET, SOCK_DGRAM)
count = 0

# connect to room ?? >> enter IP
# touch server 
# messageArray? 

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
        print("start send/confirm")
        sendMessage(self.name, self.package, self.servInf)
        print("message delivered")

def sendMessage(threadName, packet, serverDetails):
    clientSocket.sendto(packet.encode(), serverDetails)
    
    msgACK, serverAddress = clientSocket.recvfrom(2048)    
    if(msgACK.decode() == "msgLost"):
        count += 1
        if(count==10):
            help()
        sendMessage(threadName, packet, serverDetails)
        # counter and could not deliver after 10 implement
        
# hash function
def hash(message):
    return "<hK>" + str(zlib.adler32(message.encode())) + "</hK>"
# command header (not normal message)
def commandHeader(command, name):
    msgType = "<T>"+ command + "</T>"
    clientName = '<ID>' + name + '</ID>'
    return msgType + clientName
# build the packet header
def msgHeader(name, hashkey, msgNum): # client side order and reorder
    msgType = "<T>msg</T>"
    clientName = '<ID>' + name + '</ID>'
    msgHash = hashkey
    return msgType + clientName + msgHash
#quit function
def quit():
    sendMsg = commandHeader("quit", clientID)
    hashKey = hash(sendMsg)
    sendMsg += hashKey
    clientSocket.sendto(sendMsg.encode(),serverInfo)
    clientSocket.close()

def touch():
    awe

message = ''
while(True):
    message = input('msg > ')

    # if command 
    if(message[0] == '/'):
        if(message == '/quit'):
            quit()
            break # neccassary? 

        
    sendMsg = msgHeader(clientID, hash(message)) + '{' + message + '}'
    
    thread1 = sendThread(1, "Thread-1", sendMsg, serverInfo)
    thread1.start()

    # client side integrity check after broadcast
    
# new thread to listen for messages from server only if server touched.
        
clientSocket.close()

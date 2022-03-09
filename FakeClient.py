from socket import*
import zlib

# Network stuff
homeIP = "192.168.0.180"
uctIP = "196.42.86.45"
serverInfo = (homeIP, 24000) # insert own network IP
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientID = 'DieKwaaiRatel'
# clientName = input('Enter identifier:')

# hash function
def hash(message):
    return "<hK>" + str(zlib.adler32(message.encode())) + "</hK>"

# command header (not normal message)
def commandHeader(command, name):
    msgType = "<T>"+ command + "</T>"
    clientName = '<ID>' + name + '</ID>'
    return msgType + clientName

# build the packet header
def msgHeader(name, hashkey):
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

message = ''
while(True):
    message = input('msg > ')

    # if command 
    if(message[0] == '/'):
        if(message == '/quit'):
            quit()
            break # neccassary? 

        
    sendMsg = msgHeader(clientID, hash(message)) + '{' + message + '}'
    
    clientSocket.sendto(sendMsg.encode(),serverInfo)
    
    msgStatus, serverAddress = clientSocket.recvfrom(2048)
    if(msgStatus.decode() == "msgLost"):    
        clientSocket.sendto(sendMsg.encode(),serverInfo)
    else:
        continue

# new thread to listen for messages from server only if server touched.
        
clientSocket.close()
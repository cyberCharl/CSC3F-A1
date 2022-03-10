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
encryptKey = [12,35,63,75,56]
#clientID = 'DieKwaaiRatel'
clientID = input('Enter identifier:')

# (DONE)
def main():
    # touch server 
    touch(clientID, encryptKey)
    rThread = recieveThread(2, "Reciever")
    rThread.start()

    message = ''
    while(True):
        message = input('msg > ')

        # if command 
        if(message[0] == '/'):
            if(message == '/quit'):
                quit()
                break # neccassary?
     
        message = encryptMessage(message, encryptKey)
        thread1 = sendThread(1, "Thread-1", msgPacket(clientID, message), serverInfo)
        thread1.start()
    # new thread to listen for messages from server only if server touched.      
    clientSocket.close()

    
### Client-side Sending functionality (DONE)
class sendThread(thr.Thread):
    def __init__(self, threadID, name, package, servInf):
        thr.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.package = package
        self.servInf = servInf

    def run(self):
        sendMessage(self.package, self.servInf)
        
# send and check message (DONE)
def sendMessage(packet, serverDetails):
    clientSocket.sendto(packet.encode(), serverDetails)
    tic = time.perf_counter()
    
    while(time.perf_counter() - tic <= 0.5):
        msgACK, serverAddress = clientSocket.recvfrom(2048)
        
        if(msgACK.decode() == "msgLost"):
            tic = time.perf_counter()
            clientSocket.sendto(packet.encode(), serverDetails)
        else:
             break        

# command header (not normal message) (DONE)
def commandHeader(command, name):
    msgType = "<T>"+ command + "</T>"
    clientName = '<ID>' + name + '</ID>'
    return msgType + clientName

# build the message packet with header and message (DONE)
def msgPacket(name, messageContent): # client side order and reorder
    msgType = "<T>msg</T>"
    clientName = '<ID>' + name + '</ID>'
    packet = msgType + clientName + "<cnt>" + messageContent + "</cnt>"
    msgHash = hash(packet)
    return packet + msgHash

#quit function (DONE)
def quit():
    sendMsg = commandHeader("quit", clientID)
    hashKey = hash(sendMsg)
    sendMsg += hashKey
    sendMessage(sendMsg, serverInfo)
    #  clientSocket.sendto(sendMsg.encode(),serverInfo)
    clientSocket.close()

# (DONE)
def touch(name, encryptKey):
    keyString = ""
    for i in encryptKey:
        keyString += str(i)

    encKey = "<ek>" + keyString + "</ek>"
    sendMsg = commandHeader("touch", name) + encKey
    hashKey = hash(sendMsg)
    sendMsg += hashKey
    sendMessage(sendMsg, serverInfo)

# (DONE)
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


# hash function (DONE)
def hash(message):
    return "<hK>" + str(zlib.adler32(message.encode())) + "</hK>"


### Client-side Receiving

# Send and confirm thread to take messages passed to it, send to server and wait for response. 
class recieveThread(thr.Thread):
    def __init__(self, threadID,name):
        thr.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        recieveMessage()

def recieveMessage():
     while True:
        recievedMessage, serverAddress = clientSocket.recvfrom(2048)
        # packetRecv, currentClientAdd = clientSocket.recvfrom(2048)

        msgRcv = msgProtocol(recievedMessage, serverAddress)
    
        if msgRcv[0] == "down":
            print("fok soentoe")
    
        if msgRcv[0] == "msg":
            messageContent = msgRcv[2]
            print(msgRcv[1] + '>> ' + messageContent)

# parsing protocol header add counter (DONE)
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
        clientSocket.sendto("msgRcvd".encode(), serverAddress)
    else: 
        clientSocket.sendto("msgLost".encode(), serverAddress) 
        # wait for response - thread?
    
    if (msgType == "touch"):
        encKey = packet[packet.find("<ek>") + 4: packet.find("</ek>")]
        return [msgType, clientName, encKey]

    # get sent message and decrypt (would need clientID)
    msgContent = decryptMessage(packet, encryptKey)

    return [msgType, clientName, msgContent]

def checkHash(message, recievedHash): # (DONE)
    return (zlib.adler32(message.encode()) == int(recievedHash))

if __name__ == "__main__":
    main()
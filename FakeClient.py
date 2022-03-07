from socket import*
import zlib

# Network stuff

serverInfo = ("192.168.0.180", 12000) # insert own network IP
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientName = 'Tokkolosh' 
# clientName = input('Enter identifier:')

message = ''
while(message!='\quit'):
    message = input('msg > ')
    # quit function
    if(message == '\quit'):
        sendMsg = '<' + clientName + '> ' + "{" + "Disconnected}" 
        clientSocket.sendto(sendMsg.encode(),serverInfo)
        break
    msgHash = zlib.adler32(message.encode())
    sendMsg = '['+ str(msgHash) + ']' + '<' + clientName + '> ' + '{' + message + '}'
    
    clientSocket.sendto(sendMsg.encode(),serverInfo)
    
    msgStatus, serverAddress = clientSocket.recvfrom(2048)
    if(msgStatus.decode() == "msgLost"):    
        clientSocket.sendto(sendMsg.encode(),serverInfo)
    else:
        continue
        
clientSocket.close()

# def sendMessage(message):
        
#     #while(message!='\quit'):
#         #message = input('msg > ')

#         # quit function
#         if(message == '\quit'):
#             sendMsg = '<' + clientName + '> ' + 'Disconnected'
#             clientSocket.sendto(sendMsg.encode(),serverInfo)
#             terminalEntry.delete(0,'end')
#         msgHash = zlib.adler32(message.encode())
#         sendMsg = '['+ str(msgHash) + ']' + '<' + clientName + '> ' + '{' + message + '}'

#         clientSocket.sendto(sendMsg.encode(),serverInfo)
    
#         msgStatus, serverAddress = clientSocket.recvfrom(2048)
#         if(msgStatus.decode() == "msgLost"):    
#             clientSocket.sendto(sendMsg.encode(),serverInfo)
            
#         terminalPush(message)

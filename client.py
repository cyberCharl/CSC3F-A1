from pickle import FALSE
from socket import*
import tkinter as tk
from unicodedata import name
import zlib
from random import *


encryptKey = [randint(10,94), randint(10,94), randint(10,94), randint(10,94), randint(10,94)]
tScrollCounter = 0
sScrollCounter = 0

# reading from text file for server list

serverFile = open('servers.txt','r')
serverList = ['', '', '', '']
for line in serverFile:
    serverInfo = line.split(';')
    serverText = serverInfo[0] + ' -  -  - ' + serverInfo[1]
    serverList.reverse()
    serverList.insert(4, serverText)
    serverList.reverse()
serverFile.close()

# Network stuff

serverInfo = ("192.168.0.180", 12000) # insert own network IP
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientName = 'Tokkolosh' 
# clientName = input('Enter identifier:')

# create window

selected = 0
window = tk.Tk()    
window.configure(bg = 'black')

# create labels

frame = tk.Frame(bg = 'black')
title = tk.Label(master = frame, text = 'SKALLYWAG MESSENGER', fg = 'green', bg = 'black', width = 25, anchor = 'n', font = ('OCR A EXTENDED', 25))
start = tk.Label(master = frame, text = ' - Start Chat', fg = 'green', bg = 'black', width = 20, anchor = 'w', font = ('OCR A EXTENDED', 18))
servers = tk.Label(master = frame, text = ' - Servers', fg = 'green', bg = 'black', width = 20, anchor = 'w', font = ('OCR A EXTENDED', 18))  
help = tk.Label(master = frame, text = ' - Help', fg = 'green', bg = 'black', width = 20, anchor = 'w', font = ('OCR A EXTENDED', 18))

# pack labels into window

title.pack(fill = tk.X)
start.pack(fill = tk.X, pady = (40,0))
servers.pack(fill = tk.X, pady = (15,0))
help.pack(fill = tk.X, pady = (15,0))     

# chat start screen

def startStartChat():

    # defining stage for gui

    startChatWindow = tk.Tk()
    startChatWindow.configure(bg = 'black')
    startChatFrame = tk.Frame(master = startChatWindow, bg = 'black')
    startChatTitle = tk.Label(master = startChatFrame, text = 'start chat', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    startChatCodeEnter = tk.Label(master = startChatFrame, text = 'enter ip address or server id:', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    startChatIPEntry = tk.Entry(master = startChatFrame, fg = 'green', bg = 'black', width = 40, font = ('OCR A EXTENDED', 14))
    startChatNameEnter = tk.Label(master = startChatFrame, text = 'enter display name:', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    startChatNameEntry = tk.Entry(master = startChatFrame, fg = 'green', bg = 'black', width = 40, font = ('OCR A EXTENDED', 14))
    startChatTitle = tk.Label(master = startChatFrame, text = 'Start Chat', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    startChatCodeEnter = tk.Label(master = startChatFrame, text = 'Enter IP Address or Server ID:', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    startChatEntry = tk.Entry(master = startChatFrame, fg = 'green', bg = 'black', width = 40, font = ('OCR A EXTENDED', 14))

    # packing stage for gui

    startChatFrame.pack()
    startChatTitle.pack()
    startChatCodeEnter.pack(pady = (25,0))
    startChatIPEntry.pack()
    startChatNameEnter.pack(pady = (25,0))
    startChatNameEntry.pack()

    # event handlers

    def startChatEnterKey(event):
        global serverList

        for serv in serverList:
            servInfo = serv.split(' -  -  - ')
            serverName = servInfo[0]
            if serverName == startChatIPEntry.get():
                serverIP = servInfo[1]
                break
        else:
            serverIP = startChatIPEntry.get()
        
        if startChatNameEntry.get() == '':
            startChatNameEnter.config(text = 'please enter display name:')
        else:
            clientDisplayName = startChatNameEntry.get()
            chatTerminal()

    startChatWindow.bind('<Return>', startChatEnterKey)

    # start gui

    startChatWindow.mainloop()

#server screen

def startServer():
    
    # defining stage for gui

    serverWindow = tk.Tk()
    serverWindow.configure(bg = 'black')
    serverFrame = tk.Frame(master = serverWindow, bg = 'black')
    serverTitle = tk.Label(master = serverFrame, text = 'Server List', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    server1 = tk.Label(master = serverFrame, text = ' ', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    server2 = tk.Label(master = serverFrame, text = ' ', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    server3 = tk.Label(master = serverFrame, text = ' ', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    server4 = tk.Label(master = serverFrame, text = ' ', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    server5 = tk.Label(master = serverFrame, text = ' ', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    serverAdd = tk.Label(master = serverFrame, text = 'Add Server', fg = 'green', bg = 'black', width = 40, anchor = 'n', font = ('OCR A EXTENDED', 16))
    serverNameLabel = tk.Label(master = serverFrame, text = 'Server Name', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    serverNameEntry = tk.Entry(master = serverFrame, fg = 'green', bg = 'black', width = 40, font = ('OCR A EXTENDED', 14))
    serverIPLabel = tk.Label(master = serverFrame, text = 'Server IP', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    serverIPEntry = tk.Entry(master = serverFrame, fg = 'green', bg = 'black', width = 40, font = ('OCR A EXTENDED', 14))

    # packing stage for gui

    serverFrame.pack()
    serverTitle.pack()
    server1.pack(pady = (15,0))
    server2.pack(pady = (15,0))
    server3.pack(pady = (15,0))
    server4.pack(pady = (15,0))
    server5.pack(pady = (15,0))
    serverAdd.pack(pady = (20,0))
    serverNameLabel.pack(pady = (15,0))
    serverNameEntry.pack()
    serverIPLabel.pack(pady = (15,0))
    serverIPEntry.pack()

    # event handlers

    def serverScrollDown():
        global sScrollCounter

        if len(serverList) > sScrollCounter*5 + 9:
            sScrollCounter = sScrollCounter + 1
        
        k = 5*sScrollCounter
        server1.config(text = serverList[k])
        server2.config(text = serverList[k + 1])
        server3.config(text = serverList[k + 2])
        server4.config(text = serverList[k + 3])
        server5.config(text = serverList[k + 4])

    def serverScrollUp():
        global sScrollCounter

        if sScrollCounter != 0:
            sScrollCounter = sScrollCounter - 1
        
        k = 5*sScrollCounter
        server1.config(text = serverList[k])
        server2.config(text = serverList[k + 1])
        server3.config(text = serverList[k + 2])
        server4.config(text = serverList[k + 3])
        server5.config(text = serverList[k + 4])
    
    def serverAdd(serverName, serverIP):
        fileLine = '\n' + serverName + ';' + serverIP
        serverFile = open('servers.txt', 'a')
        serverFile.write(fileLine)
        serverFile.close

        serverText = serverName + ' -  -  - ' + serverIP
        serverList.reverse()
        serverList.insert(4, serverText)
        serverList.reverse()

        serverScrollUp()


    def serverUpKey(event):
        serverScrollUp()

    def serverDownKey(event):
        serverScrollDown()

    def serverEnterKey(event):
        serverAdd(serverNameEntry.get(), serverIPEntry.get())
        serverNameEntry.delete(0,'end')
        serverIPEntry.delete(0,'end')

    serverWindow.bind('<Up>', serverUpKey)
    serverWindow.bind('<Down>', serverDownKey)
    serverWindow.bind('<Return>', serverEnterKey)

    # start gui
    serverScrollUp()
    serverWindow.mainloop()

# help screen

def startHelp():

    # defining stage for gui

    helpWindow = tk.Tk()
    helpWindow.configure(bg = 'black')
    helpFrame = tk.Frame(master = helpWindow, bg = 'black')
    helpTitle = tk.Label(master = helpFrame, text = 'Help', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    help1 = tk.Label(master = helpFrame, text = 'Use the up and down arrow keys to navigate and', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help2 = tk.Label(master = helpFrame, text = 'enter to select. The \'start chat\' screen is used', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help3 = tk.Label(master = helpFrame, text = 'to connect to a chat server. The \'servers\' screen', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help4 = tk.Label(master = helpFrame, text = 'is where you can save important servers so that', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help5 = tk.Label(master = helpFrame, text = 'you won\'t have to remember their ip. The chat', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help6 = tk.Label(master = helpFrame, text = 'has several commands that you can use. Below is', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help7 = tk.Label(master = helpFrame, text = 'the full list of chat commands.', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))
    help8 = tk.Label(master = helpFrame, text = 'commands:', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    help9 = tk.Label(master = helpFrame, text = '\quit: logs you out of the chat server', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 12))

    # packing stage for gui

    helpFrame.pack()
    helpTitle.pack()
    help1.pack(pady = (15,0))
    help2.pack(pady = (15,0))
    help3.pack(pady = (15,0))
    help4.pack(pady = (15,0))
    help5.pack(pady = (15,0))
    help6.pack(pady = (15,0))
    help7.pack(pady = (15,0))
    help8.pack(pady = (20,0))
    help9.pack(pady = (15,0))

    # start gui

    helpWindow.mainloop()

def selectLabel(label):
    label.config(fg = 'black', bg = 'green')

def unselectLabel(label):
    label.config(fg = 'green', bg = 'black')

def updateLabels():
    global selected
    if selected == 0:
        selectLabel(start)
        unselectLabel(servers)
        unselectLabel(help)
    elif selected == 1:
        unselectLabel(start)
        selectLabel(servers)
        unselectLabel(help)
    else:
        unselectLabel(start)
        unselectLabel(servers)
        selectLabel(help)

# chat terminal

def chatTerminal():
    messageList = ['', '', '', '', '', '', '']
    global tScrollCounter
    tScrollCounter = 0

    # defining stage for gui

    terminalWindow = tk.Tk()
    terminalWindow.configure(bg = 'black')
    terminalFrame = tk.Frame(master = terminalWindow, bg = 'black')
    terminalTitle = tk.Label(master = terminalFrame, text = 'Chat', fg = 'green', bg = 'black', width = 40, anchor = 'n', font = ('OCR A EXTENDED', 20))
    terminalLine1 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine2 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine3 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine4 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine5 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine6 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine7 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalLine8 = tk.Label(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 50, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalEntryLabel = tk.Label(master = terminalFrame, text = '>', fg = 'green', bg = 'black', width = 1, anchor = 'w', font = ('OCR A EXTENDED', 14))
    terminalEntry = tk.Entry(master = terminalFrame, text = '', fg = 'green', bg = 'black', width = 60, relief = 'raised', font = ('OCR A EXTENDED', 14))

    # packing stage for gui

    terminalFrame.pack()
    terminalTitle.pack()
    terminalLine1.pack()
    terminalLine2.pack()
    terminalLine3.pack()
    terminalLine4.pack()
    terminalLine5.pack()
    terminalLine6.pack()
    terminalLine7.pack()
    terminalLine8.pack()
    terminalEntryLabel.pack(side = tk.LEFT)
    terminalEntry.pack(side = tk.LEFT)

    # event handlers
    
    def terminalScrollUp():
        global tScrollCounter

        if len(messageList) > tScrollCounter*8 + 15:
            tScrollCounter = tScrollCounter + 1
        
        k = 8*tScrollCounter
        terminalLine1.config(text = messageList[k + 7])
        terminalLine2.config(text = messageList[k + 6])
        terminalLine3.config(text = messageList[k + 5])
        terminalLine4.config(text = messageList[k + 4])
        terminalLine5.config(text = messageList[k + 3])
        terminalLine6.config(text = messageList[k + 2])
        terminalLine7.config(text = messageList[k + 1])
        terminalLine8.config(text = messageList[k])

    def terminalScrollDown():
        global tScrollCounter

        if tScrollCounter != 0:
            tScrollCounter = tScrollCounter - 1
        
        k = 8*tScrollCounter
        terminalLine1.config(text = messageList[k + 7])
        terminalLine2.config(text = messageList[k + 6])
        terminalLine3.config(text = messageList[k + 5])
        terminalLine4.config(text = messageList[k + 4])
        terminalLine5.config(text = messageList[k + 3])
        terminalLine6.config(text = messageList[k + 2])
        terminalLine7.config(text = messageList[k + 1])
        terminalLine8.config(text = messageList[k])

    def terminalPush(message):
        messageList.insert(0, message)
        terminalLine1.config(text = messageList[7])
        terminalLine2.config(text = messageList[6])
        terminalLine3.config(text = messageList[5])
        terminalLine4.config(text = messageList[4])
        terminalLine5.config(text = messageList[3])
        terminalLine6.config(text = messageList[2])
        terminalLine7.config(text = messageList[1])
        terminalLine8.config(text = messageList[0])
        terminalEntry.delete(0,'end')

    def sendMessage(message):
        
    #while(message!='\quit'):
        #message = input('msg > ')

        # quit function
        # if(message == '\quit'):
        #     sendMsg = '<' + clientName + '> ' + 'Disconnected'
        #     clientSocket.sendto(sendMsg.encode(),serverInfo)
        #     terminalEntry.delete(0,'end')
        # msgHash = zlib.adler32(message.encode())
        # sendMsg = '['+ str(msgHash) + ']' + '<' + clientName + '> ' + '{' + message + '}'

        # clientSocket.sendto(sendMsg.encode(),serverInfo)
    
        # msgStatus, serverAddress = clientSocket.recvfrom(2048)
        # if(msgStatus.decode() == "msgLost"):    
        #     clientSocket.sendto(sendMsg.encode(),serverInfo)
            
        terminalPush(message)

    def terminalEnterKey(event):
        sendMessage(terminalEntry.get())
    
    def terminalUpKey(event):
        terminalScrollUp()

    def terminalDownKey(event):
        terminalScrollDown()
        
    terminalWindow.bind('<Up>', terminalUpKey)
    terminalWindow.bind('<Down>', terminalDownKey)
    terminalWindow.bind('<Return>', terminalEnterKey)

    # start gui

    terminalWindow.mainloop()

# encryption and decryption

def encryptMessage(message, key):
    keycount = 0
    output = ''

    for i in message:           # loop through the characters in the message
        icode = ord(i) + key[keycount]   # convert the character into ascii code and then add the correct part of the key
        
        if icode > 126:                 # roll ascii code over if it's too high
            icode = (icode - 126) + 31
        
        keycount = keycount + 1         # increment the part of the key
        if keycount == 5:               # or roll it over if it has reached the end of the key
            keycount = 0

        output = output + chr(icode)    # convert the ascii code back into a char and append it to the output string
    
    return output

def decryptMessage(message, key):
    keycount = 0
    output = ''

    for i in message:
        icode = ord(i) - key[keycount]   # the decryption is identical to the encryption above, except it
                                         # subtracts the part of the key instead of adding it
        if icode < 32:
            icode = (icode + 126) - 31   # which means it also checks if the code is too low rather than too high
        
        keycount = keycount + 1
        if keycount == 5:
            keycount = 0

        output = output + chr(icode)
    
    return output

# main screen event handlers

def upKey(event):
    global selected
    if selected != 0:
        selected = selected - 1
    else:
        selected = 2
    updateLabels()
    title.config(text = encryptMessage(title.cget('text'), encryptKey))

def downKey(event):
    global selected          
    if selected != 2:
        selected = selected + 1
    else:
        selected = 0
    updateLabels()
    title.config(text = encryptMessage(title.cget('text'), encryptKey))

def enterKey(event):
    global selected
    if selected == 0:
        startStartChat()
    elif selected == 1:
        startServer()
    else:
        startHelp()

window.bind('<Up>', upKey)
window.bind('<Down>', downKey)
window.bind('<Return>', enterKey)

frame.pack(fill = tk.X)
updateLabels()
window.mainloop()    # start the GUI


# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# clientSocket.close()

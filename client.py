from socket import*
import tkinter as tk
from unicodedata import name
import zlib

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
title = tk.Label(master = frame, text = 'hackerman messenger', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 25))
start = tk.Label(master = frame, text = ' - start chat', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 18))
accomplices = tk.Label(master = frame, text = ' - accomplices', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 18))  
options = tk.Label(master = frame, text = ' - options', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 18))

# pack labels into window

title.pack(fill = tk.X)
start.pack(fill = tk.X, pady = (40,0))
accomplices.pack(fill = tk.X, pady = (15,0))
options.pack(fill = tk.X, pady = (15,0))     
accomplices.pack(fill = tk.X,)
options.pack(fill = tk.X)

# event handlers

def startStartChat():

    # defining stage

    startChatWindow = tk.Tk()
    startChatWindow.configure(bg = 'black')
    startChatFrame = tk.Frame(master = startChatWindow, bg = 'black')
    startChatTitle = tk.Label(master = startChatFrame, text = 'start chat', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    startChatCodeEnter = tk.Label(master = startChatFrame, text = 'enter chat code or accomplice id:', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    startChatEntry = tk.Entry(master = startChatFrame, text = 'enter chat code or accomplice id:', fg = 'green', bg = 'black', width = 40, font = ('OCR A EXTENDED', 14))

    # packing stage

    startChatFrame.pack()
    startChatTitle.pack()
    startChatCodeEnter.pack(pady = (25,0))
    startChatEntry.pack(pady = (25,0))

    # start gui

    startChatWindow.mainloop()

def startAccomplice():

    # defining stage

    accompliceWindow = tk.Tk()
    accompliceWindow.configure(bg = 'black')
    accompliceFrame = tk.Frame(master = accompliceWindow, bg = 'black')
    accompliceTitle = tk.Label(master = accompliceFrame, text = 'accomplice list', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    accompliceOne = tk.Label(master = accompliceFrame, text = 'accomplice1', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    accompliceTwo = tk.Label(master = accompliceFrame, text = 'accomplice2', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    accompliceThree = tk.Label(master = accompliceFrame, text = 'accomplice3', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    accompliceFour = tk.Label(master = accompliceFrame, text = 'accomplice4', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    accompliceFive = tk.Label(master = accompliceFrame, text = 'accomplice5', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))

    # packing stage

    accompliceFrame.pack()
    accompliceTitle.pack()
    accompliceOne.pack(pady = (15,0))
    accompliceTwo.pack(pady = (15,0))
    accompliceThree.pack(pady = (15,0))
    accompliceFour.pack(pady = (15,0))
    accompliceFive.pack(pady = (15,0))

    # start gui

    accompliceWindow.mainloop()

def startOptions():

    # defining stage

    optionWindow = tk.Tk()
    optionWindow.configure(bg = 'black')
    optionFrame = tk.Frame(master = optionWindow, bg = 'black')
    optionTitle = tk.Label(master = optionFrame, text = 'option list', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 20))
    optionOne = tk.Label(master = optionFrame, text = 'option1', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    optionTwo = tk.Label(master = optionFrame, text = 'option2', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    optionThree = tk.Label(master = optionFrame, text = 'option3', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    optionFour = tk.Label(master = optionFrame, text = 'option4', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))
    optionFive = tk.Label(master = optionFrame, text = 'option5', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 14))

    # packing stage

    optionFrame.pack()
    optionTitle.pack()
    optionOne.pack(pady = (15,0))
    optionTwo.pack(pady = (15,0))
    optionThree.pack(pady = (15,0))
    optionFour.pack(pady = (15,0))
    optionFive.pack(pady = (15,0))

    # start gui

    optionWindow.mainloop()

def selectLabel(label):
    label.config(fg = 'black', bg = 'green')

def unselectLabel(label):
    label.config(fg = 'green', bg = 'black')

def updateLabels():
    global selected
    if selected == 0:
        selectLabel(start)
        unselectLabel(accomplices)
        unselectLabel(options)
    elif selected == 1:
        unselectLabel(start)
        selectLabel(accomplices)
        unselectLabel(options)
    else:
        unselectLabel(start)
        unselectLabel(accomplices)
        selectLabel(options)


def upKey(event):
    global selected
    if selected != 0:
        selected = selected - 1
    else:
        selected = 2
    updateLabels()

def downKey(event):
    global selected          
    if selected != 2:
        selected = selected + 1
    else:
        selected = 0
    updateLabels()

def enterKey(event):
    global selected
    if selected == 0:
        startStartChat()
    elif selected == 1:
        startAccomplice()
    else:
        startOptions()

def debugTerminal(event):

    # defining stage

    terminalWindow = tk.Tk()
    terminalWindow.configure(bg = 'black')
    terminalFrame = tk.Frame(master = terminalWindow, bg = 'black')
    terminalTitle = tk.Label(master = terminalFrame, text = 'chat', fg = 'green', bg = 'black', width = 40, anchor = 'n', font = ('OCR A EXTENDED', 20))
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

    # packing stage

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

    def terminalPush(message):
        terminalLine1.config(text = terminalLine2.cget('text'))
        terminalLine2.config(text = terminalLine3.cget('text'))
        terminalLine3.config(text = terminalLine4.cget('text'))
        terminalLine4.config(text = terminalLine5.cget('text'))
        terminalLine5.config(text = terminalLine6.cget('text'))
        terminalLine6.config(text = terminalLine7.cget('text'))
        terminalLine7.config(text = terminalLine8.cget('text'))
        terminalLine8.config(text = message)
        terminalEntry.delete(0,'end')
        

    def sendMessage(message):
        
    #while(message!='\quit'):
        #message = input('msg > ')

        # quit function
        if(message == '\quit'):
            sendMsg = '<' + clientName + '> ' + 'Disconnected'
            clientSocket.sendto(sendMsg.encode(),serverInfo)
            terminalEntry.delete(0,'end')
        msgHash = zlib.adler32(message.encode())
        sendMsg = '['+ str(msgHash) + ']' + '<' + clientName + '> ' + '{' + message + '}'

        clientSocket.sendto(sendMsg.encode(),serverInfo)
    
        msgStatus, serverAddress = clientSocket.recvfrom(2048)
        if(msgStatus.decode() == "msgLost"):    
            clientSocket.sendto(sendMsg.encode(),serverInfo)
            
        terminalPush(message)

    def terminalEnterKey(event):
        sendMessage(terminalEntry.get())
        

    terminalWindow.bind('<Return>', terminalEnterKey)

    # start gui

    terminalWindow.mainloop()

window.bind('<Up>', upKey)
window.bind('<Down>', downKey)
window.bind('<Return>', enterKey)
window.bind('<BackSpace>', debugTerminal)

frame.pack(fill = tk.X)
updateLabels()
window.mainloop()    # start the GUI


modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
clientSocket.close()

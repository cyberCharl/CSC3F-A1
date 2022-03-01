from socket import*
import tkinter as tk
from unicodedata import name

window = tk.Tk()    # create window
window.configure(bg = 'black')
frame = tk.Frame(bg = 'black')
title = tk.Label(master = frame, text = 'hackerman messenger', fg = 'green', bg = 'black', width = 30, anchor = 'n', font = ('OCR A EXTENDED', 25))
start = tk.Label(master = frame, text = ' - start chat', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 18))
accomplices = tk.Label(master = frame, text = ' - accomplices', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 18))  # create labels
options = tk.Label(master = frame, text = ' - options', fg = 'green', bg = 'black', width = 40, anchor = 'w', font = ('OCR A EXTENDED', 18))
title.pack(fill = tk.X)
start.pack(fill = tk.X, pady = (40,0))     # pack labels into window
accomplices.pack(fill = tk.X,)
options.pack(fill = tk.X)
frame.pack(fill = tk.X)
window.mainloop()    # start the GUI

# serverName = 'hostname'
# serverPort = 12000
# clientSocket = socket(AF_INET, SOCK_DGRAM)

# message = input('Input sentence:')
# clientSocket.sendto(message.encode(),(serverName, serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# print (modifiedMessage.decode())
# clientSocket.close()
# CSC3F-A1
Assignment 1 - Create chat app with custom protocol

## Mission Satement
Client-Server chat app. Intention of this assignment is to create a privacy focussed chat app that allows people to communicate annonamously with each other. The messages are only visible while the sender of said messages is connected to the server. Once the person leaves, all the messages that they have sent will be removed and will not be recoverable.

## Main features
- Messages that delete upon sender leaving the chat.
- Messages are not recoverable.
- Identitfier of an user is randomly assigned upon log-on, however
- Encryption

## Protocol Design
- Message confirmation 
    Hash message before sending, attach key with message, hash message upon recieve, if keys match, send server confirm and display message. Else request message resend. 
- Protocol structure:
    - Header end: ```\n```
    - clientName field: ```<ID>clientName</ID>```
    - messageTypes: ```<T>type</T>```
        - Touch/Connect (touch)
        - MessageContent ```<cnt>Message</cnt>```
        - Quit/Disconnect (leave)
    - hashKey: ```<hK>key</hK>```

## Running of the program
    -To run the program, simply enter the following 
    command into the Bourne Again Shell:
        python3 "path_to_script"/client.py

    You will now see the GUI
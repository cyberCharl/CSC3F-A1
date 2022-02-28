# CSC3F-A1
Assignment 1 - create chat app with custom protocol

    Kwaai soos 'n ratel
    Die chello is mellow
    

## Mission Satement
Client-Server chat app. Intention of this assignment is to create a privacy focussed chat app that allows people to communicate annonamously with each other. The messages are only visible while the sender of said messages is connected to the server. Once the person leaves, all the messages that they have sent will be removed and will not be recoverable.

## Main features
- Messages that delete upon sender leaving the chat.
- Messages are not recoverable.
- Identitfier of an user is randomly assigned upon log-on, however "Accomplices" will still be able to contact the user.
- ```/obliterate``` command will forcefully delete all messages in the group (only admins can use)

## Protocol Design
- ???
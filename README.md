# PYTHON Chat Room
## Multi-User Chat-Room Application.
## BY **MOHAMED ALGHALY**

Multi-Threaded and Multi-User Chat-Room application, with user/Administrator privileges using Python.

# Video Goes HERE

## Overall look on the application

### The Big Picture

This is a chat room application based on server-client model, where multiple clients are connected to a single server.

**There are two types of clients:**

1. A user with no extra privileges, only sends and receives messages.
2. An admin with extra privileges like kicking a user from the chat room or banning a user from connecting to the chat-room.

## How does the application work
1. When the server runs it starts listening to upcoming connections.
3. When a client connects to the chat-room ask him for a username.
3. If the username represents one of the admins, the admin is required to verify his identity with his password.
4. If a wrong password is given refuse the connection for that client, else log him in.
5. The client now can interact in the chat-room with his allowable actions.
6. When any client sends a message it is broadcasted to the chat-room for all clients to see.
7. Any client can safely disconnect from the room and the other clients will be notified.
8. An admin can kick any user, and he will be kicked from the chat room with the ability to rejoin and the other clients will be notified.
9. An admin can ban any user, and he will be kicked from the chat-room without the ability to rejoin and the other clients will be notified.
10. A user cannot execute admin commands.

## Code explaining (the project design)
### NOTE
> I have included comments to every single line in the code to explain what that line does, and we will go through the code here again.

> We have two files in our project, one for the server and one for the client.

### The Server Code
1. First, we import the socket package to handle socket connections.
2. Import the threading package to be able to give a single thread for each client so the server can work with all clients in parallel.
3. We start initializing the constants we will use in the code like the host which will be our device so the IP address for the host will be the local host IP address, the port which represents any unused port in our device, the code which is the encoding format which we will use in the channel, and we will use the celebrity UTF- 8, the admins for our chat room, the address for the server which is a tuple of the IP and the port, and three empty list one for the clients in the channel and another to store the banned users and one to store the usernames.
4. We define the server socket and bind it with the address of our device
5. Start listening to incoming connections.
6. Then we define a kick function to handle what happens when an admin kicks a user:
   1. Assure that you are kicking an actual connected user.
   2. Remove the client associated with that username from the clients list and remove its username from the usernames list.
   3. Let the kicked user knows he is kicked and let the other clients know as will.
   4. Disconnect that user from the chat-room.
7. Define a function to handle the broadcasting functionality:
    * As simple as sending a message to all connected clients.
8. Define a function to handle the functionality for a single client in an infinite loop to keep running as long as the server is running:
    1. Get a message from the server and decode it to see its content.
    2. If the message is a kick command:
        1. Check if the client has the access to that command, if so kick that user from the channel.
        2. Otherwise tell the client that his command is refused.
    3. If the message is a ban command:
        1. Check if the client has access to that command, if so kick that user from the channel.
        2. Add his name to the list of banned users.
        3. Otherwise tell the client that his command is refused.
    4. If the message is not a command message, just broadcast it.
    5. In case of any errors during the operation, which is because the user is disconnected just remove the client from the clients list, remove its username from the usernames list, close his connection, let the other clients know he has disconnected and break from the loop.
9. Define a receive function to handle the connection for a single client in an infinite loop to keep running as long as the server is running:
    1. Accept the incoming connection from the client.
    2. Send that client a request for ausername.
    3. Receive the username and decode it.
    4. If that user is banned, send him a banned message and close the connection.
    5. If the client is admin, send him a request for his password and if the given password is wrong just let him know and close the connection.
    6. Add the username to the usernames list and the client to the clients list and let the others know that they had a company.
    7. Let the user himself know he has just connected successfully to the server.
10. Define a thread to handle the functionality for that client.
11. Start the thread.
12. When the server runs, start receiving connections.
---
<br>

## The client code:
1. First,we import the socket package to handle socket connections.
2. Import the threading package to be able to give a single thread for sending messages and another for receiving, so the client can send and receive at the same time.
3. We start initializing the constants we will use in the code like the host, will be our device so the IP address for the host will be the local host IP address, the port which represents any unused port in our device, the code which isthe encoding format which we will use in the channel, and we will use the celebrity UTF- 8, the admins for our chat room, the address for the client, which is a tuple of the IP and the port, and finally a flag to keep track of the state of the user.
4. Ask the client for a username, and if an admin username is given ask him for his password.
5. Define the client socket and connect it with the address of our device.
6. Define the function for receiving messages in an infinite loop to keep receiving new messages.
    1. If the user is kicked or banned stop receiving (the user state is true).
    2. Receive the incoming message and decode it.
    3. Receive the second message ifthere is one.
    4. If the second message asks for a passwords end the password to server.
    5. If the server replied with a refuse message as the password is wrong set the state for that user to true.
    6. If the server replied with a ban message set the state for that user to true.
    7. If the first message is not a request message just add it to the client's chat-room.
    8. In case of any error just let the client know, close the connection, and stop receiving.
7. Define the function for sending messages in an infinite loop to keep sending new messages.
    1. If the user is kicked or banned stop receiving (the user state is true).
    2. Take the message to send from the user.
    3. If the message is a command and the client is privileged to execute commands send the command to the server to be executed.
    4. If a normal message is to be sent just add the username of the client to it, and send it to the server.
8. Define two threads, one for sending functionality and one for receiving, then start both.
import socket
import threading  # to handle multi threading in python so clients can work in parallel

# CONSTANTS:
host = "127.0.0.1"  # Local Host
port = 5050  # any free port
code = 'utf-8'  # the encoding format
address = (host, port)  # the address of the server
admins = {'admin1': '12345', 'admin2': '13579', 'admin3': '2468'}  # the username and password for the admins.
banned = []  # a list containing the banned usernames

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # build the server socket
server.bind(address)  # bind the socket to our local device as the server
server.listen()  # start listening to upcoming connections

clients = []  # all the current clients in the chat room
user_names = []  # the user names for the connected clients


def kick(user):
    """
    :param user: the user name we want to kick
    :return: if the user is privileged to do so the user specified will be kicked out of the chat room
    """
    if user in user_names:  # check we have a valid username to kick
        index = user_names.index(user)  # get the index for that username
        client = clients[index]  # get the client associated with that user
        clients.remove(client)  # remove that client from the client list
        client.send("YOU WERE KICKED BY AN ADMIN !!".encode(code))  # let the user know that he has been kicked
        client.close()  # close the connection with that client
        user_names.remove(user)  # remove the username from usernames list
        broadcast(f'{user} WAS KICKED FROM THE CHAT ROOM BY AN ADMIN !!'.encode(code))  # let the other clients know


def broadcast(message):
    """
    :param message: The message to broadcast
    :return: nothing just broadcast the message to all the connected clients
    """
    for client in clients:
        client.send(message)  # send that message to all the connected clients


def handle(client):
    """
    :param client: the client
    :return: nothing just to handle the connection for a client
    """
    while True:
        try:  # while the user is successfully connected
            msg = message = client.recv(2048)  # receive any upcoming message from the client
            msg = msg.decode(code)
            if msg.startswith("KICK"):  # if the message is a kick command
                if user_names[clients.index(client)] in admins:  # if the user has admin privileges
                    name_to_kick = msg[5:]  # get the username to kick
                    kick(name_to_kick)  # kick that user
                else:  # if the user is not privileged refuse the command
                    client.send("COMMAND WAS REFUSED!!".encode(code))  # let the user knows that his command is refused
            elif msg.startswith("BAN"):  # if the message is a ban command
                if user_names[clients.index(client)] in admins:  # if the user has admin privileges
                    name_to_ban = msg[4:]   # get the username to ban
                    kick(name_to_ban)  # kick that user
                    banned.append(name_to_ban)  # add its name to the banned list
                    print(F"{name_to_ban} WAS BANNED")
                else:
                    client.cend("COMMAND WAS REFUSED!!".encode(code))  # let the user knows that his command is refused
            else:  # in case of a non command message
                broadcast(message)  # broadcast it
        except:  # in case of disconnection
            if client in clients:  # if the client is not already kicked
                index = clients.index(client)  # find the disconnected client
                clients.remove(client)  # remove the client from the clients list
                client.close()  # close the connection for that user
                username = user_names[index]  # get its username
                user_names.remove(username)  # remove its username from the usernames list
                broadcast(f'{username} left the chat ....'.encode(code))  # let the others know that this client has just disconnected
                break  # stop receiving from this client


def receive():
    while True:
        client, address = server.accept()  # accept clients all the time
        print(f"CONNECTED WITH {address} .....")  # let the server admin know that a client has connected
        client.send('USERNAME?'.encode(code))  # ask the client for a username
        username = client.recv(1024).decode(code)  # get the username from the client

        if username in banned:  # if the username is banned
            client.send('BANNED'.encode(code))  # let the user knows he is banned
            client.close()  # close the connection for that user
            continue  # end this iteration

        if username in admins:  # if admin tries to login ask for his password
            client.send("PASSWORD?".encode(code))  # let the user knows that we asked for his password
            password = client.recv(1024).decode(code)  # receive the password

            if password != admins[username]:  # check the password
                client.send('REFUSED'.encode(code))  # if wrong password send refuse the connection
                client.close()
                continue

        user_names.append(username)  # add the username for that client to the list of our usernames
        clients.append(client)  # add the client to the list of our clients
        print(f'THE NICKNAME FOR THIS USER IS {username}')  # let the server admin knows the username for the client
        broadcast(f'{username} has just joined the chat .....'.encode(code))  # let the chat room users know who has just joined
        client.send('CONNECTED TO THE SERVER ...'.encode(code))  # let the client itself knows he has just connected to the server
        thread = threading.Thread(target=handle, args=(client,))  # lets handle that client
        thread.start()  # each client works in its own thread so the users can chat in parallel


print("SERVER IS LISTENING ........")  # let the server admin know that the server has started listening
receive()  # start the chat room


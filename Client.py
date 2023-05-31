import socket
import threading  # to handle multi threading in python so clients can work in parallel

host = "127.0.0.1"  # our local host
port = 5050  # any unused port
address = (host, port)  # the address of the client
code = 'utf-8'  # the encoding format
admins = ['admin1', 'admin2', 'admin3']  # the admins for the chat room
stop = False  # a flag to keep track if the user is kicked from the chat room

username = input("ENTER YOUR USERNAME ")  # let the user pick a username
if username in admins:  # in case of admin login
    password = input('ENTER YOUR PASSWORD : ')  # ask for a password


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # build the client socket
client.connect(address)  # connect that socket to the server


def receive():
    """
        always be ready to receive a new message from the server
    """
    global stop  # the flag
    while True:
        if stop:  # if the user is kicked stop receiving
            break
        try:
            message = client.recv(2048).decode(code)  # receive any incoming messages from the server
            if message == 'USERNAME?':  # if the server is asking for your username
                client.send(username.encode(code))  # send him the username that the user has just picked
                next_message = client.recv(2048).decode(code)  # receive the next message from the server
                if next_message == 'PASSWORD?':  # if the server asked for a password
                    client.send(password.encode(code))  # send it the password
                    if client.recv(1024).decode(code) == 'REFUSED':  # if the server refused the connection
                        print("CONNECTION WAS REFUSED WRONG PASSWORD !!!")  # let the client know that
                        stop = True  # set the flag to true
                elif next_message == 'BANNED':  # in case of a ban message
                    print("CONNECTION REFUSED BECAUSE OF A BAN !!")  # let the client know
                    stop = True  # set the flag to true
            else:
                print(message)  # let the user read the message from the server
        except:  # in case of any errors just close the connection
            print("AN ERROR OCCURRED !!")
            client.close()
            break


def send():
    """
        always be ready to send a new message to the server
    """
    while True:  # always wait for the user to send a new message
        if stop:  # if the user is kicked stop sending new messages
            break
        message = input("")  # take the message from the user

        if message.startswith('/'):  # in case of a command message
            if username in admins:  # assure we have admin privileges
                if 'kick' in message.lower() or 'ban' in message.lower():
                    client.send(f'{message[1:5].upper()}{message[5:]}'.encode(code))  # send the command to the server
                else:
                    print("INVALID COMMAND !!!!!!!!!")
            else:
                print("THIS COMMAND CAN ALSO BE EXECUTED BY ADMINS !!!!!!")  # in case we don't have admin access
        else:  # a non command message
            message = username + " : " + message  # add his identity to the message
            client.send(message.encode(code))  # send the message to the server


receive_thread = threading.Thread(target=receive)  # a thread for receiving new messages
receive_thread.start()
send_thread = threading.Thread(target=send)  # a thread for sending new messages
send_thread.start()


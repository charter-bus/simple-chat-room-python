# Import the threading and socket modules
import threading
import socket

# Define the host and port to be used
host = socket.gethostname()
port = 55555

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", port))
server.listen()

# Lists for Clients and their Nicknames
clients = []
nicknames = []

# Define a function to broadcast a message to all Clients.

def broadcast(message):
    for client in clients:
        client.send(message)

# Define a function to handle the messages from Clients.

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Tearing down connections with clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{}left the chat!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
# Define a function to listen for data on the bound socket
def receive():
    while True:
        client, address = server.accept()
        print("Connected with{}".format(str(address)))

        # Request and Store Nickname
        client.sent('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        # Nickname received. Store it, and check if it is already in use
        #! Implement name check function
        nicknames.append(nickname)
        clients.append(client)

        # Print and Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined the chat!".format(nickname).encode('ascii'))
        client.send('Connected to the chat room server!'.encode('ascii'))

        # Start Handling Thread for Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Add a function to check if the nickname is already in use

# def checkNameList(desiredNickname):
#    for nickname in nicknames:
#        if nickname == "":
#           return False
print("Server is listening...")
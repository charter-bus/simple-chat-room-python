import socket
import threading

nickname = input("Desired Nickname: ")

# Choosing Nickname, and Connecting to the Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 55555
client.bind(("", port))
client.connect((host, port))

# Listening to the Server and Sending the Nickname
def receive():
    while True:
        try:
            #Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error ocurred!")
            client.close()
            break
# Implement a function to accept input from the client, and write it to the server.
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
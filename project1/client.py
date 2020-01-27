import socket

server_ip_address = 'localhost'

# If you change below information, You must also change them in server.py also to program work correctly
server_port = 12000
MSS=128

# Initializing socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip_address, server_port))
# Send configuration massage
client_socket.send("connection setup request".encode())
# Receive ACK
buf = client_socket.recv(MSS).decode()
if buf == "connection being established":
    # cli implementation
    print("Hi, You are connected to server, You can send your computing expressions (type exit to exit")
    massage = input()
    # Exit situation checked
    exit_bool = (massage == "exit")
    while not exit_bool:
        client_socket.send(massage.encode())
        # Output showed on screen
        print(client_socket.recv(MSS).decode())
        massage = input()
        # update exit situation
        exit_bool = (massage == "exit")
    client_socket.send(massage.encode())

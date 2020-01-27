# Note that i handle the project without use of offset, but I need to add extra chars("$end$") representing the end_
# of_file. I also recommend to read my first project in order to understand my code structure better.

import socket

server_ip_address = '127.0.0.1'
server_port = 4000
client_port = 8000
file_name_max_size = 100


def serve_response(args):
    print("Serving file...")
    serve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serve_socket.bind((server_ip_address, server_port))
    msg, client_address = serve_socket.recvfrom(file_name_max_size)
    print("Client connected...")
    # args[3] represent name of the file
    if msg.decode() == args[3]:
        # args[3] represent path of the file
        data_file = open(args[5])
        text = data_file.read(128)
        while True:
            # Check to see if can add "$end$" to the last part of massage or we need to add another segment
            if text.__len__() <= 123:
                text = text + "$end$"
                serve_socket.sendto(text.encode(), client_address)
                break
            elif not data_file:
                serve_socket.sendto(text.encode(), client_address)
                serve_socket.sendto("$end$".encode(), client_address)
                break
            else:
                # default segments send command
                serve_socket.sendto(text.encode(), client_address)
            text = data_file.read(128)
        print("File transfers to client, The end!")
    else:
        serve_socket.sendto("Not such a file exist in server".encode(), client_address)
    serve_socket.close()


# This function will be used to check if we reach end of file
def check_exit_condition(massage):
    if "$end$" in massage:
        return True
    return False


def receive_request(args):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.sendto(args[2].encode(), (server_ip_address, server_port))

    file = open("output_data_"+args[2], "w")
    msg_from_server = udp_client_socket.recvfrom(128)
    msg = msg_from_server[0].decode()
    exit_bool = check_exit_condition(msg)
    while True:
        if exit_bool:
            file.write(msg.replace("$end$", ""))
            break
        else:
            file.write(msg)
        msg_from_server = udp_client_socket.recvfrom(128)
        msg = msg_from_server[0].decode()
        exit_bool = check_exit_condition(msg)


command = input()
arguments = command.split(" ")

while True:
    try:
        if arguments[1] == "-receive":
            receive_request(arguments)
            break
        elif arguments[1] == "-serve":
            serve_response(arguments)
            break
        else:
            print("Not such a command! Try again...")
            command = input()
            arguments = command.split()
    except:
        print("Something wrong, Try again!")
        command = input()
        arguments = command.split()


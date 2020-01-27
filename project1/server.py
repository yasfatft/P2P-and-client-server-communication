import math
import socket
import threading

server_ip_address = 'localhost'
max_clients_connection=5

# If you change below information, You must also change them in client.py also to program work correctly.
server_port = 12000
MSS=128


# here are the list of functions (iterations) we can do in server
def add(operator_1, operator_2):
    return float(operator_1) + float(operator_2)


def subtract(operator_1, operator_2):
    return float(operator_1) - float(operator_2)


def divide(operator_1, operator_2):
    return float(operator_1) / float(operator_2)


def multiply(operator_1, operator_2):
    return float(operator_1) * float(operator_2)


def sin(operator):
    return math.sin(float(operator))


def cos(operator):
    return math.cos(float(operator))


def tan(operator):
    return math.tan(float(operator))


def cot(operator):
    return 1 / tan(operator)


# Simple switcher (string to func).
def switch(command):
    if command[0] == "Add":
        return add(command[1], command[2])
    elif command[0] == "Subtract":
        return subtract(command[1], command[2])
    elif command[0] == "Divide":
        return divide(command[1], command[2])
    elif command[0] == "Multiply":
        return multiply(command[1], command[2])
    elif command[0] == "Sin":
        return sin(command[1])
    elif command[0] == "Cos":
        return cos(command[1])
    elif command[0] == "Tan":
        return tan(command[1])
    elif command[0] == "Cot":
        return cot(command[1])
    # If something else return False as error.
    return False


# This func will be used to separate important keywords from others($) and also parsing string (I try not to be so
# serious about request syntax(However if there was a problem in syntax I asked client to try again with correct one
def command_parsing(command):
    command_pars = command.replace("$", " ")
    # Separate extra marks
    command_pars = command_pars.split(" ")
    # Deleting extra spaces
    command_pars = [word for word in command_pars if word.__len__() > 0]
    return command_pars


# Use this function for calculate math expression and find result
def execute_command(command):
    command_parsed = command_parsing(command)
    return switch(command_parsed)


def single_socket_thread_handling(connection, client_id):
    global clients_connected
    # buf is in charge of input massages
    buf = connection.recv(MSS).decode()
    if buf == "connection setup request":
        connection.send("connection being established".encode())
        buf = connection.recv(MSS).decode()
        exit_bool = (buf == "exit")
        while not exit_bool:
            # Don't do any action for empty auto sent massage
            if buf != '':
                try:
                    result = execute_command(buf)
                    if result is False:
                        connection.send("Something went wrong!\nTry  again.".encode())
                    else:
                        connection.send(str(result).encode())
                    buf = connection.recv(MSS).decode()
                    exit_bool = (buf == "exit")
                except:
                    connection.send("Something went wrong!\nTry  again.".encode())
                    buf = connection.recv(MSS).decode()
                    exit_bool = (buf == "exit")
    print("connection # "+str(client_id)+" closed")
    clients_connected-=1


# initializing server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', server_port))
server_socket.listen(max_clients_connection)

clients_connected=0
client_id=0
connections_threads=[]
while True:
    if clients_connected<max_clients_connection:
        simple_connection, address = server_socket.accept()
        clients_connected+=1
        print("Client # "+str(client_id)+" connects!")
        temp_thread=threading.Thread(target=single_socket_thread_handling, args=(simple_connection, client_id))
        client_id+=1
        connections_threads.append(temp_thread)
        temp_thread.start()

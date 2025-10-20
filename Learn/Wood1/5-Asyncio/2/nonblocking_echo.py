import socket
import select

IP = "127.0.0.1"
PORT = 9001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #   Makes a new socket when a new client joins
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #   Lets you reuse the port/IP after a restart no need to wait
server_socket.bind((IP, PORT))
server_socket.listen()
server_socket.setblocking(False)    #   Makes a non blocking server

sockets_list = [server_socket]
clients = {}

print(f"Non-blocking server listening on port {PORT} ...")

while True:
    print("---DEBUG SOCKET_LIST---")
    print(sockets_list)

    print("---DEBUG CLIENTS DICTIONARY---")
    print(clients)

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)  #   LOOK AT NOTES.TXT
    
    for notified_socket in read_sockets:                                #   Reads the read_socket list
        if notified_socket == server_socket:                            #   If in read_sockets theres a server_socket then : (refere to the NOTES.txt)
            client_socket, client_address = server_socket.accept()      #   socket is the unique identifier and the address is there ip and port
            client_socket.setblocking(False)                            #   Sets non blocking client
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"New connection from {client_address}")
            print("---DEBUG NOTIFIED_SOCKET 1---")
            print(notified_socket)
        else:
            print("---DEBUG NOTIFIED_SOCKET 1---")
            print(notified_socket)
            data = notified_socket.recv(1024)
            if data:
                print(f"Received from {clients[notified_socket]}: {data.decode()}")
                notified_socket.sendall(b"ECHO: " + data)
            else:
                print(f"Connection closed from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()
        

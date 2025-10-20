import socket
c = socket.socket()
c.connect(('127.0.0.1', 9000))
c.sendall(b'hello')
response = c.recv(1024)
print(f"Server response: {response}")
c.close()

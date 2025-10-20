import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = b"Hello UDP"
client.sendto(message, ('127.0.0.1', 9002))

response, addr = client.recvfrom(1024)
print(f"Server response: {response.decode()}")
client.close()
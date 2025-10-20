import asyncio

async def handle_client(reader, writer):    # Handles Client connections
    client_addr = writer.get_extra_info('peername')     # Gets clients IP and Port
    print(f"New connection from {client_addr}")     # ('127.0.0.1', 44336)
    
    try:    # Error handling block
        while True:
            data = await reader.read(100)   # Will read up to 100 bytes
            if not data:    # Check if client disconnected 
                break
            message = data.decode().strip()     # Converts bytes into string
            print(f"Received from {client_addr}: {message}")    # Log the message
            
            writer.write(f"ECHO: {message}\n".encode())     # Encodes sting to bytes to send through a network
            await writer.drain()    # Waits for all the bytes to be sent
            
    except Exception as e:  # Catch errors
        print(f"Error with {client_addr}: {e}")     # Logs errors
    finally:    #   Finally will always run
        print(f"Connection closed from {client_addr}")  # Logs the closed connection
        writer.close()      # Close the TCP connection
        await writer.wait_closed()      # Waits until the socket is actully closed

async def main():
    server = await asyncio.start_server(    # Create TCP Server object
        handle_client, '127.0.0.1', 9001
    )
    addr = server.sockets[0].getsockname()  # Chsoses the first thing in the socket list which is addr 
    print(f"Server listening on {addr}")
    print(server)
    
    async with server:
        await server.serve_forever()    # Starts server indefinitely

if __name__ == "__main__":
    asyncio.run(main())

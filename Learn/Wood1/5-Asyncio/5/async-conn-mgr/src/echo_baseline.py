import asyncio

async def handle_clients(reader, writer):
    client_addr = writer.get_extra_info("peername")
    print(f"New connection from {client_addr}")
    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode().strip()
            print(f"Client {client_addr} sent {message}")

            writer.write(f"ECHO : {message}".encode())
            await writer.drain()
    except Exception as e:
        print(f"Client : {client_addr} failed : {e}")

    finally:
        print(f"{client_addr} closed connection")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_clients, "127.0.0.1", 9001
    )
    print(f"server listening on localhost and on port 9001")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
import asyncio, signal

class connectionManager:
    def __init__(self): # Used to initialise the variables for the class
        self.active = set() # List that's unordered, doesn't allow duplicates and is optimised for speed
        self.shutting_down = False

    async def add(self, writer):
        if self.shutting_down:
            writer.close()
            await writer.wait_closed()
            return False
        self.active.add(writer)
        print(f"active: {len(self.active)}")
        return True
    
    def remove(self, writer):
        if writer in self.active:
            self.active.remove(writer)
            print(f"Active : {len(self.active)}")

    async def close_all(self):
        self.shutting_down = True
        print(f"\nClosing {len(self.active)} connections...")
        for w in self.active:
            w.close()
        if self.active:
            await asyncio.gather(*(w.wait_closed() for w in list(self.active)), return_exceptions=True) # What the fuck is this
        print("All connections closed")

mgr = connectionManager()

async def handle_client(reader, writer):
    if not await mgr.add(writer):   # No clue bro
        return
    addr = writer.get_extra_info("peername")
    print(f"New: {addr}")
    try:
        while True:
            try:
                data = await asyncio.wait_for(reader.read(100), timeout=30.0)
            except asyncio.TimeoutError:
                print(f"Timeout {addr}")
                break
            if not data:
                print(f"Graceful close {addr}")
                break
            msg = data.decode().strip()
            writer.write(f"ECHO: {msg}\n".encode())
            await writer.drain()
    except ConnectionResetError:    # Dont know
        print(f"Abrupt {addr}")
    finally:
        mgr.remove(writer)
        writer.close()
        await writer.wait_closed()

# No idea what main does

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 9001)
    loop = asyncio.get_running_loop()   # No clue 
    stop = asyncio.Event()  # What the bro
    def on_signal():
        print("\nSignal -> shutdown...")
        stop.set()  # what does this even mean

    #   After this dont know
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, on_signal)
    print("Server on localhost:9001 - Ctrl + C to stop")
    async with server:
        await stop.wait()
        server.close()
        await server.wait_closed()
        await mgr.close_all()
    print("Shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())
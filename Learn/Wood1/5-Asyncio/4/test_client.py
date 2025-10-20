import asyncio
import time

async def test_client(client_id, message="hello"):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 9001)
        start_time = time.time()
        
        writer.write(f"{message} from {client_id}\n".encode())
        await writer.drain()
        
        data = await reader.read(100)
        response = data.decode().strip()
        
        latency = (time.time() - start_time) * 1000
        print(f"Client {client_id}: {response} (latency: {latency:.1f}ms)")
        
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"Client {client_id} failed: {e}")

async def main():
    # Test with increasing concurrency
    print("Testing with 1 client...")
    await test_client(1)
    
    print("\nTesting with 5 clients...")
    await asyncio.gather(*(test_client(i) for i in range(5)))
    
    print("\nTesting with 20 clients...")
    await asyncio.gather(*(test_client(i) for i in range(20)))

if __name__ == "__main__":
    asyncio.run(main())
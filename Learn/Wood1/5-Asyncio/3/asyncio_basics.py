import asyncio
import time

async def say_after(delay, message):    # Define a coroutine function 
    await asyncio.sleep(delay) 
    print(message)
    return f"Completed: {message}"

async def sequential_tasks():
    print("--- Running sequentially ---")
    start = time.time()
    
    result1 = await say_after(1, "Hello")
    result2 = await say_after(1, "World")
    
    print(f"Sequential took: {time.time() - start:.2f}s")   # .2f means 2 digits after the decimal point
    return [result1, result2]

async def concurrent_tasks():
    print("--- Running concurrently ---")
    start = time.time()
    
    task1 = asyncio.create_task(say_after(1, "Hello"))
    task2 = asyncio.create_task(say_after(1, "World"))
    
    results = await asyncio.gather(task1, task2)
    print(f"Concurrent took: {time.time() - start:.2f}s")
    return results

async def main():
    # Run sequentially
    seq_results = await sequential_tasks()
    print(f"Sequential results: {seq_results}\n")
    
    # Run concurrently  
    con_results = await concurrent_tasks()
    print(f"Concurrent results: {con_results}")

if __name__ == "__main__":
    asyncio.run(main())
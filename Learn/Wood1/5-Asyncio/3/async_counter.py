import asyncio

async def counter(name):

    n = 1
    number = 1

    while n < 4:
        print(number)
        number += 1
        n += 1
        await asyncio.sleep(0.5)

    print(f"Finsihed {name}")

async def main():
    await asyncio.gather(*(counter(i) for i in range(5)))

asyncio.run(main())


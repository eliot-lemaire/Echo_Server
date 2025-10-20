import asyncio
import random

async def fetchWeather(Country):
    print(f"Fetching data for {Country}")
    await asyncio.sleep(1)
    print(f"The temperature in {Country} is {random.randint(10, 30)} degrees celcius")

async def main():
    print("Starting program...")
    await asyncio.gather(
        fetchWeather("Brazil"),
        fetchWeather("France"),
        fetchWeather("Iceland")
    )

if __name__ == "__main__":
    asyncio.run(main())
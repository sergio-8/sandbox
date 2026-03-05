import asyncio
import time

async def coffee(brew, delay):
    print(f"-> Starting to Make {brew} coffee (takes {delay}s)...")
    await asyncio.sleep(delay)
    print(f"<- {brew} coffee is ready!")
    return f"{brew} cup"

async def main():
    start = time.perf_counter()
    
    print("Kitchen is open! Starting orders...")
    
    # asyncio.gather schedules both coroutines to run concurrently
    # It waits for the longest task to complete
    results = await asyncio.gather(
        coffee("Dark Roast", 3),
        coffee("Light Roast", 2),
        coffee("Espresso", 1)
    )
    
    end = time.perf_counter()
    
    print(f"\nOrders served: {results}")
    print(f"Total time elapsed: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
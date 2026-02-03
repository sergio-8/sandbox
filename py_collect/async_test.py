import time
import asyncio


#Define make_coffee as an async function.

async def coffee(brew, delay):

    print(f"Starting to Make {brew} coffee...")

# Use asyncio.sleep(3) inside it.

    await asyncio.sleep(delay)


#Create a main() function to await the coffee.

async def main():
    start = time.perf_counter()
    await coffee("dark roast", 3)
    end = time.perf_counter()
    print(f"Made {brew} coffee in {end - start} seconds.")

#Execute it using asyncio.run().    
    

if __name__ == "__main__":
    asyncio.run(main())
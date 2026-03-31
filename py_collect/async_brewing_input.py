import asyncio
import time

async def coffee(brew, delay):
    print(f"-> Starting to Make {brew} coffee (takes {delay}s)...")
    await asyncio.sleep(delay)
    print(f"<- {brew} coffee is ready!")
    return f"{brew} cup"

async def main():
    user_input = input("What would you like to order? (americano, latte, espresso): ")
    orders = user_input.lower().replace(',', ' ').split()
    tasks = []

    for order in orders:
        if "americano" in order:
            tasks.append(coffee("Americano", 5))
        elif "latte" in order:
            tasks.append(coffee("Latte", 3))
        elif "espresso" in order:
            tasks.append(coffee("Espresso", 2))
        else:
            print(f"Sorry, we don't have '{order}'.")
    
    start = time.perf_counter()
    
    if tasks:
        await asyncio.gather(*tasks)


    end = time.perf_counter()
    print(f"Total time elapsed: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
        
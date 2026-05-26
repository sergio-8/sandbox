import asyncio
import httpx # An async-compatible library for web requests

async def get_status(url):
    async with httpx.AsyncClient() as client:
        # 'await' here lets other URLs be checked while waiting for the server
        response = await client.get(url)
        return f"{url}: {response.status_code}"

async def main():
    urls = ["https://google.com", "https://github.com", "https://python.org"]
    
    # Using the same 'gather' pattern you learned!
    tasks = [get_status(u) for u in urls]
    results = await asyncio.gather(*tasks)
    
    for r in results:
        print(r)

if __name__ == "__main__":
    asyncio.run(main())
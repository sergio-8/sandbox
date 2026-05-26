import asyncio
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

model = "gemini-3-flash-preview"

agent = Agent(
   model=model,
   name='currency_exchange_agent',
)
app = AdkApp(agent=agent)

async def main():
    async for event in app.async_stream_query(
       user_id="123456",
       message="What is the exchange rate from US dollars to EURO currency as of today 2026-03-07?",
    ):
       pass
    
    # Try closing the session or app if applicable
    if hasattr(app, 'close'):
        await app.close()

if __name__ == "__main__":
    asyncio.run(main())

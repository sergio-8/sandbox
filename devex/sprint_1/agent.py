model = "gemini-2.5-flash"

from google.genai import types

safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
]

generate_content_config = types.GenerateContentConfig(
   safety_settings=safety_settings,
   temperature=0.28,
   max_output_tokens=1000,
   top_p=0.95,
)

import asyncio
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

agent = Agent(
   model=model,                                      # Required.
   name='currency_exchange_agent',                   # Required.
   generate_content_config=generate_content_config,  # Optional.
)
app = AdkApp(agent=agent)

async def main():
    async for event in app.async_stream_query(
       user_id="123456",  # Required
       message="What is the current or latest exchange rate from US dollars to EURO currency? Pay attention : I'm not interested in a  specific date",
    ):
       try:
           # If event is a dataclass/object with attributes or a dict
           if isinstance(event, dict):gecrt
               parts = event.get('content', {}).get('parts', [])
               for part in parts:
                   if 'text' in part:
                       print(part['text'], end='', flush=True)
           else:
               # Handle it as an object
               if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                   for part in event.content.parts:
                       if hasattr(part, 'text'):
                           print(part.text, end='', flush=True)
       except Exception:
           pass
    print()  # Add a newline at the end

if __name__ == "__main__":
    asyncio.run(main())
   

   
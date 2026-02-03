from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()

# Configuration
APP_NAME = "kaggle_test_agent"
USER_ID = "test_user"
SESSION_ID = "session_001"
MODEL_NAME = "gemini-2.0-flash-001"

# Initialize Agent (Keep at top level for deployment)
agent = Agent(
    name="kaggle_researcher",
    model=MODEL_NAME,
    description="A basic researcher agent for Kaggle tasks.",
    instruction="You are a helpful data science assistant. Provide concise and accurate info.",
)

async def chat_with_agent(runner, query):
    """Interacts with the agent using the new async pattern."""
    print(f"User: {query}")
    
    content = types.Content(role='user', parts=[types.Part(text=query)])
    # We use run_async to be consistent with modern ADK
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print(f"Agent: {response_text}")
            return response_text

async def main():
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found. Please set it in your .env file.")
        return

    # Setup Session and Runner inside main to avoid import side-effects
    session_service = InMemorySessionService()
    # Await the session creation to fix the RuntimeWarning
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

    query = input("Enter your query: ")
    await chat_with_agent(runner, query)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

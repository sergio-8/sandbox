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
MODEL_NAME = "gemini-flash-latest"

# Initialize Agent
agent = Agent(
    name="kaggle_researcher",
    model=MODEL_NAME,
    description="A basic researcher agent for Kaggle tasks.",
    instruction="You are a helpful data science assistant. Provide concise and accurate info.",
)

# Setup Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

def chat_with_agent(query):
    """Simple wrapper to interact with the agent."""
    print(f"User: {query}")
    
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print(f"Agent: {response_text}")
            return response_text

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found. Please set it in your .env file.")
    else:
        query = input("Enter your query: ")
        chat_with_agent(query)

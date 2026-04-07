import asyncio
import os
import uuid
from agent import get_bigquery_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

APP_NAME = "bq_agent_local"
USER_ID = "local_user_01"

async def run_conversation(prompt: str):
    """Runs a conversation with the BigQuery agent using the ADK Runner."""
    
    session_service = InMemorySessionService()
    session_id = f"{APP_NAME}-{uuid.uuid4().hex[:8]}"
    root_agent = get_bigquery_agent()

    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    
    final_response_text = "Unable to retrieve final response."
    tool_calls = []

    print(f"\nUser: {prompt}")
    print("Agent: Thinking...")

    try:
        # Run the agent and process events
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        ):
            if (
                event.content
                and event.content.parts
                and event.content.parts[0].function_call
            ):
                func_call = event.content.parts[0].function_call
                print(f"\n[Tool Call] -> {func_call.name}")
                print(f"Args: {dict(func_call.args)}")

            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                    break

    except Exception as e:
        print(f"Error in conversation: {e}")
        final_response_text = f"An error occurred: {e}"

    print(f"\nFinal Response:\n{final_response_text}")
    return final_response_text

if __name__ == "__main__":
    # Test question
    prompt = "What tables are available in the dataset?"
    asyncio.run(run_conversation(prompt))

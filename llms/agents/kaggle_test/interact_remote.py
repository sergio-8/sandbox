import vertexai
from vertexai import agent_engines
import os
from dotenv import load_dotenv

# Initialize Vertex AI
PROJECT_ID = "sv-ml-sandbox"
LOCATION = "us-central1"
# The new Resource ID after redeployment with valid model name
REMOTE_AGENT_ID = 'projects/412996116194/locations/us-central1/reasoningEngines/1206240121972588544'

vertexai.init(project=PROJECT_ID, location=LOCATION)

def query_remote_agent(prompt):
    print(f"Connecting to remote agent...")
    remote_agent = agent_engines.get(REMOTE_AGENT_ID)
    
    print(f"User: {prompt}")
    
    # ADK Agents use 'stream_query' with 'message' and 'user_id' instead of 'query'
    print("\n--- Remote Agent Response ---")
    try:
        response_stream = remote_agent.stream_query(
            message=prompt, 
            user_id="default-user"
        )
        
        for event in response_stream:
            # ADK events are returned as dictionaries. We look for 'content' in the event.
            if isinstance(event, dict) and 'content' in event:
                parts = event['content'].get('parts', [])
                for part in parts:
                    if 'text' in part:
                        print(part['text'], end="", flush=True)
            elif isinstance(event, dict) and 'actions' in event:
                # This could be tool calls or internal status updates
                pass
                
    except Exception as e:
        print(f"\nError during remote query: {e}")
        
    print("\n" + "-" * 30)

if __name__ == "__main__":
    user_query = input("Ask your remote agent: ")
    if user_query:
        query_remote_agent(user_query)

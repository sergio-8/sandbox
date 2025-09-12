"""Creating a test search VAIS agent for proptotyping purrpose."""


import asyncio



from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools import VertexAiSearchTool


YOUR_SEARCH_ENGINE_ID = "projects/sv-ml-sandbox/locations/global/collections/default_collection/engines/bl-test-1_1730215399951"
YOUR_DATASTORE_ID =  "projects/sv-ml-sandbox/locations/global/collections/default_collection/datastore/bl-ds-test-1_1730215462525"

# Constants
APP_NAME_VSEARCH = "vertex_search_app"
USER_ID_VSEARCH = "user_vsearch_1"
SESSION_ID_VSEARCH = "session_vsearch_1"
AGENT_NAME_VSEARCH = "doc_qa_agent"
GEMINI_2_FLASH = "gemini-2.0-flash-exp"

# Tool Instantiation
# You MUST provide your datastore ID here.
vertex_search_tool = VertexAiSearchTool(search_engine_id=YOUR_SEARCH_ENGINE_ID)

root_agent = LlmAgent(
    name=AGENT_NAME_VSEARCH,
    model=GEMINI_2_FLASH, # Requires Gemini model
    tools=[vertex_search_tool],
    instruction=f"""You are a helpful assistant that answers questions based on
    information found using the search engine {YOUR_SEARCH_ENGINE_ID} to find
    relevant information before answering.
    Your primary knowledge is contained in the search  engine: {YOUR_SEARCH_ENGINE_ID}. If the answer you are looking for isn't in the documents, say that you couldn't find the information.
    If you find ambiguous or contradictory data in the documents report the ambiguity upfront and quote the documents sources of the ambiguity, instead of trying to resolve the ambiguity.
    """,
    description="Answers questions using a specific Vertex AI Search datastore.",
)


# Session and Runner Setup
session_service_vsearch = InMemorySessionService()
runner_vsearch = Runner(
    agent=root_agent,
    app_name=APP_NAME_VSEARCH,
    session_service=session_service_vsearch,
)
session_vsearch = session_service_vsearch.create_session(
    app_name=APP_NAME_VSEARCH,
    user_id=USER_ID_VSEARCH,
    session_id=SESSION_ID_VSEARCH,
)


async def call_vsearch_agent_async(query):
  """Calls the Vertex AI Search agent with the given query.

  Args:
      query (str): The user query.
  """
  print("\n--- Running Vertex AI Search Agent ---")
  print(f"Query: {query}")
  if "YOUR_DATASTORE_ID_HERE" in YOUR_DATASTORE_ID:
    print(
        "Skipping execution: Please replace YOUR_DATASTORE_ID_HERE with "
        "your actual datastore ID."
    )
    print("-" * 30)
    return

  content = types.Content(role="user", parts=[types.Part(text=query)])
  final_response_text = "No response received."
  try:
    async for event in runner_vsearch.run_async(
        user_id=USER_ID_VSEARCH,
        session_id=SESSION_ID_VSEARCH,
        new_message=content,
    ):
      # Like Google Search, results are often embedded in the
      # model's response.
      if event.is_final_response() and event.content and event.content.parts:
        final_response_text = event.content.parts[0].text.strip()
        print(f"Agent Response: {final_response_text}")
        # You can inspect event.grounding_metadata for source citations
        if event.grounding_metadata:
          print(
              "  (Grounding metadata found with "
              f"{len(event.grounding_metadata.grounding_attributions)} "
              "attributions)"
          )

  except ValueError as e:
    print(f"A value error occurred: {e}")
    print("Please ensure that the query is valid.")
  except Exception as e:
    print(f"An error occurred: {e}")
    print(
        "Ensure your datastore ID is correct and the service account has"
        " permissions."
    )
  print("-" * 30)


async def run_vsearch_example():
  """Runs an example of the Vertex AI Search agent."""
  # Replace with a question relevant to YOUR datastore content
  await call_vsearch_agent_async(
      "Summarize the main points about the Q2 strategy document."
  )
  await call_vsearch_agent_async(
      "What safety procedures are mentioned for lab X?"
  )


# Execute the example
# await run_vsearch_example()

# Running locally due to potential colab asyncio issues with multiple awaits
try:
  asyncio.run(run_vsearch_example())
except RuntimeError as e:
  if "cannot be called from a running event loop" in str(e):
    print(
        "Skipping execution in running event loop (like Colab/Jupyter). Run"
        " locally."
    )
  else:
    raise e




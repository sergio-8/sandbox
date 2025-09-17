"""Defines the Demo Agent."""

import os
from google.adk.agents import llm_agent
import vertexai

# pylint: disable=g-import-not-at-top
if os.environ.get("IMPORT_FROM_GOOGLE3"):
  from google3.cloud.ml.discoveryengine.agents.cloudia.cloudia import get_flags
  from google3.cloud.ml.discoveryengine.agents.cloudia.cloudia import prompts
  from google3.cloud.ml.discoveryengine.agents.cloudia.cloudia import tools
else:
  from . import get_flags
  from . import prompts
  from . import tools

vertexai.init(project=get_flags.PROJECT, location=get_flags.LOCATION)

root_agent = llm_agent.Agent(
    model=get_flags.MODEL,
    name="demo_agent",
    description=(
        "Helpful assistant for answering questions using information from"
        " documentation"
    ),
    instruction=prompts.ROOT_AGENT_PROMPT,
    tools=[
        tools.get_answer_results,
        tools.authenticate_user,
        tools.update_state,
        tools.get_state],
)


# ... (all your existing code from agent.py)

# This block will only run when you execute: python -m demo_agent.agent
if __name__ == "__main__":
    print("Agent script executed successfully!")
    print(f"Loaded agent named: '{root_agent.name}'")
    print(f"Agent Description: {root_agent.description}")

    # Here you would add logic to start a server or run the agent
    # For example:
    # agent.main() or agent.start_server()
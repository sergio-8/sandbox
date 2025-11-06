# demos/demo1/agentic_modules/sub_agents/safety_agent/__init__.py

# Import the agent's properties and the agent instance itself from agent.py
from .agent import name, description, tools, safety_agent

# The ADK framework expects an `invoke` function at the module level.
# We can expose the `invoke` method of our `Agent` instance to fulfill this.


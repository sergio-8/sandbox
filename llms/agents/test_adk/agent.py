from google.adk.agents import Agent

root_agent = Agent(
name="my_new_agent",
model="gemini-2.0-flash",
description="A base agent.",
instruction="You are a helpful assistant.",
)

#Agent.ListModels()

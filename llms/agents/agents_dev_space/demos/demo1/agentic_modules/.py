# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import logging
from dotenv import load_dotenv
from typing import Optional
from google.genai import types
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.cloud import modelarmor_v1
from google.adk.tools import google_search
from google.adk.models import LlmResponse, LlmRequest
from google.adk.sessions import InMemorySessionService
from google.adk.agents.callback_context import CallbackContext
from .prompts import return_instructions_root
from .tools import (
    ask_vertex_retrieval,
    simple_before_model_modifier,
    comprehensive_before_model_guardrail,
    pii_scrubbing_callback,
    response_validation_callback,
)


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
template_model_id = os.getenv("TEMPLATE_MODEL_ARMOR_ID")

client = modelarmor_v1.ModelArmorClient(
    transport="rest",
    client_options={"api_endpoint": "modelarmor.us.rep.googleapis.com"},
)

APP_NAME = "Analyzer"
USER_ID = "Maria"
SESSION_ID = USER_ID

# Initialize session_service once globally to persist state across generate_content calls
global_session_service = InMemorySessionService()


async def setup_session_and_runner(agent):
    session = await global_session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    if session:
        print(f"Retrieved existing session: {SESSION_ID}")
    else:
        session = await global_session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
        print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=agent, app_name=APP_NAME, session_service=global_session_service
    )
    return session, runner


# RAG Agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="ask_rag_agent",
    instruction=return_instructions_root(),
    tools=[ask_vertex_retrieval],
    # before_model_callback=simple_before_model_modifier,       # This is just the keyword guardrails
    before_model_callback=comprehensive_before_model_guardrail,  # Comprehensive before model guardrails: keyword and model armor
    # after_model_callback=pii_scrubbing_callback,        # This is the callback to scrub LLM output for PII
    after_model_callback=response_validation_callback,  # Comprehensive after model callback: safety agent
)


async def generate_content(prompt: str):
    session, runner = await setup_session_and_runner(root_agent)

    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    events = runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    )

    final_response = None
    async for event in events:
        print(event)
        if event.is_final_response() and event.content and event.content.parts:
            logger.info(
                f"Potential final response from [{event.author}]: {event.content.parts[0].text}"
            )
            final_response = event.content.parts[0].text
    return final_response

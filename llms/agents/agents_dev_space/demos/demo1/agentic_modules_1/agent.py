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


from google.adk.agents import Agent
from .prompts import return_instructions_root
from .tools import (

    before_model_callback,
    comprehensive_before_model_guardrail,
    pii_scrubbing_callback,
    response_validation_callback,
)

# RAG Agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="ask_rag_agent",
    instruction=return_instructions_root(),
    before_model_callback=before_model_callback,  # Safety guardrails
    # before_model_callback=comprehensive_before_model_guardrail,  # Comprehensive before model guardrails: keyword and model armor
    # after_model_callback=pii_scrubbing_callback,        # This is the callback to scrub LLM output for PII
    after_model_callback=response_validation_callback,  # Comprehensive after model callback: safety agent
)

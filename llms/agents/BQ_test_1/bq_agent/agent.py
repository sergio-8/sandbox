"""Main BigQuery NL2SQL agent definition."""

import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types

from .prompts import get_system_prompt
from .tools import list_tables_and_schema

load_dotenv()  # load .env if present

logger = logging.getLogger(__name__)

# ── BigQuery built-in toolset (read-only) ────────────────────────────────────
# WriteMode.BLOCKED prevents the agent from running INSERT/UPDATE/DELETE/DROP.
_bq_tool_config = BigQueryToolConfig(
    write_mode=WriteMode.BLOCKED,
    application_name="bq-nl2sql-agent",
)

_bq_toolset = BigQueryToolset(
    # Only expose the execute_sql tool; other BQ toolset tools are opt-in.
    tool_filter=["execute_sql"],
    bigquery_tool_config=_bq_tool_config,
)

# ── Root agent ────────────────────────────────────────────────────────────────
root_agent = LlmAgent(
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    name="bq_nl2sql_agent",
    description=(
        "Translates natural-language questions into BigQuery SQL and executes "
        "them, returning results in a human-readable format."
    ),
    instruction=get_system_prompt(),
    tools=[
        list_tables_and_schema,  # custom schema-discovery tool
        _bq_toolset,              # ADK built-in: execute_sql (read-only)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,          # deterministic SQL generation
    ),
)

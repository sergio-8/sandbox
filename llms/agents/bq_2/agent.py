import os
from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
import google.auth
import dotenv

# Load environment variables from .env
dotenv.load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "placeholder-project-id")
DATASET_NAME = os.environ.get("BIGQUERY_DATASET", "placeholder-dataset-name")

# 1. Setup Authentication (Uses Application Default Credentials)
credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=credentials)

# 2. Instantiate the BigQuery Toolset
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config
)

# 3. Define the Agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="bigquery_agent",
    description="Agent that answers questions about BigQuery data by executing SQL queries.",
    instruction=(
        f"""
        You are a data analysis agent with access to several BigQuery tools.
        Use the appropriate tools to fetch relevant BigQuery metadata and execute SQL queries.
        You must use these tools to answer the user's questions.
        Run these queries in the project-id: '{PROJECT_ID}' on the `{DATASET_NAME}` dataset.
        Always verify the schema before running complex queries.
        """
    ),
    tools=[bigquery_toolset]
)

def get_bigquery_agent():
    return root_agent

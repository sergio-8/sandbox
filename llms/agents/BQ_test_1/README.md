# BigQuery NL2SQL Agent (ADK)

A ready-to-run [Google ADK](https://google.github.io/adk-docs/) Python agent that lets you query any BigQuery dataset using plain English. It translates natural-language questions into BigQuery Standard SQL, executes them, and returns results + insights — all in a conversational interface.

**Ultimate goal:** deploy to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) with a single script.

---

## Project structure

```
BQ_test_1/
├── bq_agent/
│   ├── __init__.py     # exposes root_agent (ADK entry point)
│   ├── agent.py        # LlmAgent definition + BigQueryToolset (read-only)
│   ├── tools.py        # list_tables_and_schema helper
│   └── prompts.py      # system instruction
├── deploy.py           # one-shot Agent Engine deployment
├── pyproject.toml      # dependencies
├── .env.example        # env var template → copy to .env
└── README.md
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Python ≥ 3.11 | `python3 --version` |
| Google Cloud project | BigQuery API enabled |
| A BigQuery dataset | Any dataset you own or have `roles/bigquery.dataViewer` on |
| `gcloud` CLI | [Install](https://cloud.google.com/sdk/docs/install) |
| Application Default Credentials | `gcloud auth application-default login` |

---

## 1 · Installation

```bash
# Clone / copy this folder, then:
cd BQ_test_1

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

---

## 2 · Configuration

```bash
cp .env.example .env
```

Open `.env` and fill in **your** values:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=1          # 1 = Vertex AI (ADC), 0 = API key
GOOGLE_CLOUD_PROJECT=my-project      # your GCP project ID
GOOGLE_CLOUD_LOCATION=us-central1   # Vertex AI region
BQ_DATASET_ID=my_dataset            # the dataset to query
BQ_LOCATION=US                       # BQ data location
```

> **Authentication**: the agent uses Application Default Credentials.
> Run `gcloud auth application-default login` if you haven't already.

---

## 3 · Run locally

### Web UI (recommended)

```bash
adk web
```

Open [http://localhost:8000](http://localhost:8000), select **bq_agent**, and start chatting.

### Terminal / CLI

```bash
adk run bq_agent
```

### Example questions you can ask

```
What tables are in my dataset?
Show me the first 10 rows of [table_name].
How many rows does [table] have?
What is the total revenue by month for 2024?
Which customers placed more than 5 orders?
```

---

## 4 · Deploy to Vertex AI Agent Engine

### 4a · Enable APIs & grant permissions

```bash
export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export RE_SA="service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"

# BigQuery read access for the Reasoning Engine service account
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${RE_SA}" --role="roles/bigquery.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${RE_SA}" --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${RE_SA}" --role="roles/aiplatform.user"
```

### 4b · Create a GCS staging bucket (one-time)

```bash
gcloud storage buckets create gs://${PROJECT_ID}-agent-staging \
  --location=us-central1
```

Then add to your `.env`:

```dotenv
AGENT_ENGINE_DISPLAY_NAME=bq-nl2sql-agent
STAGING_BUCKET=gs://YOUR_PROJECT-agent-staging
```

### 4c · Deploy

```bash
python deploy.py
```

On success you'll see:

```
✅ Deployed successfully!
   Resource name: projects/123.../locations/us-central1/reasoningEngines/456...
```

**Save the resource name** — you need it to call or delete the agent.

### 4d · Call the deployed agent

```python
import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(project="YOUR_PROJECT", location="us-central1")

agent = reasoning_engines.ReasoningEngine("projects/.../reasoningEngines/...")
session = agent.create_session(user_id="me")

response = agent.send_message(
    message="Show me the top 5 tables by row count",
    session_id=session["id"],
)
print(response["output"])
```

### 4e · Clean up

```bash
python deploy.py --delete projects/.../reasoningEngines/...
```

---

## How it works

```
User question
     │
     ▼
 LlmAgent (gemini-2.0-flash)
     │
     ├─► list_tables_and_schema()   ← discovers your BQ schema
     │
     └─► execute_sql(sql)           ← ADK BigQueryToolset (read-only)
              │
              ▼
         BigQuery API
              │
              ▼
     Formatted table + insight
```

1. On first interaction the agent calls `list_tables_and_schema` to understand what data exists.
2. It generates valid BigQuery Standard SQL.
3. It executes the SQL via the ADK built-in `execute_sql` tool (write operations are **blocked**).
4. Results are returned as a markdown table with a plain-English summary.

---

## Security notes

- `WriteMode.BLOCKED` prevents the agent from modifying any data (no INSERT / UPDATE / DELETE / DROP).
- Credentials are never sent to the LLM — only query results are.
- Never commit `.env` to source control (add it to `.gitignore`).

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `google.auth.exceptions.DefaultCredentialsError` | Run `gcloud auth application-default login` |
| `403 Access Denied` on BQ | Check your IAM roles on the dataset |
| `ModuleNotFoundError: google.adk` | Run `pip install -e .` in the venv |
| Agent Engine deploy fails | Ensure `STAGING_BUCKET` exists and you have Storage Object Creator on it |

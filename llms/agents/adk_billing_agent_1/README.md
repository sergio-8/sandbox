# ADK Billing Agent

This is an experimental billing agent built using the Google Agent Development Kit (ADK). It provides a natural language interface to query BigQuery datasets containing billing information.

## Project Structure

This project follows the recommended ADK directory layout:

```
adk_billing_agent_1/
├── agent_package/          # Core agent logic
│   ├── __init__.py
│   ├── agent.py            # Orchestrator and agent definition
│   ├── prompts.py          # System instructions and templates
│   └── tools.py            # BigQuery interaction tools
├── .env                    # Environment variables (local dev)
├── pyproject.toml          # Dependency management (Poetry)
└── README.md               # Project documentation
```

## Setup

1.  **Environment Variables**:
    *   Update the `.env` file in the root directory with your actual Google Cloud project and BigQuery dataset IDs:
        ```env
        GCP_PROJECT_ID=your-project-id
        BQ_DATASET_ID=your-dataset-id
        ```

2.  **Dependencies**:
    *   This project uses Poetry for dependency management. Install dependencies with:
        ```bash
        poetry install
        ```

## Running Locally

To run the agent locally, you can use the ADK CLI.

1.  Run the agent using `poetry run`:
    ```bash
    poetry run adk web .
    ```

    Or activate the virtual environment first:
    ```bash
    source .venv/bin/activate
    adk web .
    ```

    Or if ADK supports running from the current directory:
    ```bash
    adk run agent_package.agent:billing_agent
    ```

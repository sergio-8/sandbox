#!/usr/bin/env python3
"""Deploy the BQ NL2SQL agent to Vertex AI Agent Engine.

Usage:
    python deploy.py [--delete RESOURCE_NAME]

Prerequisites:
    1. pip install -e .
    2. gcloud auth application-default login
    3. Fill in .env with GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION,
       BQ_DATASET_ID, and STAGING_BUCKET.
    4. Grant Agent Engine SA permissions (see README.md).

The script will print the deployed resource name on success.
Save it — you'll need it to interact with or delete the agent later.
"""

import argparse
import os

from dotenv import load_dotenv

load_dotenv()

import vertexai  # noqa: E402  (must come after env load)
from vertexai.preview import reasoning_engines  # noqa: E402

from bq_agent import root_agent  # noqa: E402


def deploy(project: str, location: str, staging_bucket: str, display_name: str) -> str:
    """Package and deploy root_agent to Agent Engine.

    Args:
        project: GCP project ID.
        location: GCP region (e.g. "us-central1").
        staging_bucket: GCS URI used to stage the agent package.
        display_name: Human-readable name for the Agent Engine resource.

    Returns:
        The fully-qualified Agent Engine resource name.
    """
    vertexai.init(project=project, location=location, staging_bucket=staging_bucket)

    print(f"Deploying '{display_name}' to Agent Engine in {project}/{location} …")
    print(f"Staging bucket: {staging_bucket}")

    remote_agent = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=False,
    )

    deployed = reasoning_engines.ReasoningEngine.create(
        reasoning_engine=remote_agent,
        display_name=display_name,
        requirements=[
            "google-adk>=1.0",
            "google-cloud-bigquery>=3.0",
            "db-dtypes>=1.4",
            "google-cloud-aiplatform[adk,agent-engines]>=1.93.0",
            "python-dotenv>=1.0",
        ],
        # Pass env vars needed inside Agent Engine at runtime
        env_vars={
            "GOOGLE_CLOUD_PROJECT": project,
            "BQ_DATASET_ID": os.environ.get("BQ_DATASET_ID", ""),
            "BQ_LOCATION": os.environ.get("BQ_LOCATION", "US"),
            "GOOGLE_GENAI_USE_VERTEXAI": "1",
            "AGENT_MODEL": os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
        },
    )

    resource_name = deployed.resource_name
    print(f"\n✅ Deployed successfully!")
    print(f"   Resource name: {resource_name}")
    print("\nTo chat with the deployed agent:")
    print(f"  remote_agent = reasoning_engines.ReasoningEngine('{resource_name}')")
    print("  session = remote_agent.create_session(user_id='me')")
    print("  remote_agent.send_message(message='What tables do I have?', session_id=session['id'])")
    return resource_name


def delete(resource_name: str) -> None:
    """Delete a deployed Agent Engine resource."""
    engine = reasoning_engines.ReasoningEngine(resource_name)
    engine.delete(force=True)
    print(f"✅ Deleted: {resource_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy / manage the BQ NL2SQL agent on Agent Engine.")
    parser.add_argument("--delete", metavar="RESOURCE_NAME", help="Delete an existing deployment by resource name.")
    args = parser.parse_args()

    if args.delete:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        staging_bucket = os.environ.get("STAGING_BUCKET", "")
        vertexai.init(project=project, location=location, staging_bucket=staging_bucket)
        delete(args.delete)
    else:
        deploy(
            project=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
            staging_bucket=os.environ.get("STAGING_BUCKET", ""),
            display_name=os.environ.get("AGENT_ENGINE_DISPLAY_NAME", "bq-nl2sql-agent"),
        )

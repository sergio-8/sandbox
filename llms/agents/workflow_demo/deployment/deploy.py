import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from absl import app
from absl import flags
from demo_agent.agent import root_agent
import dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp


load_dotenv = dotenv.load_dotenv
# Get the directory where this deploy.py script lives.
_DEPLOY_DIR = os.path.dirname(os.path.abspath(__file__))

# The name of the wheel file.
AGENT_WHL_FILE_NAME = "demo_agent-0.1-py3-none-any.whl"

# The full, absolute path to the wheel file.
AGENT_WHL_FILE_PATH = os.path.join(_DEPLOY_DIR, AGENT_WHL_FILE_NAME)

FLAGS = flags.FLAGS

flags.DEFINE_string("project_id", None, "GCP project ID")
flags.DEFINE_string("location", None, "GCP location")
flags.DEFINE_string("bucket", None, "GCS bucket")
flags.DEFINE_bool("create", False, "Create a new remote agent")
flags.DEFINE_bool("delete", False, "Delete a remote agent")
flags.DEFINE_string("resource_id", None, "Resource ID of the remote agent")


def create() -> None:
  adk_app = AdkApp(
      agent=root_agent,
      enable_tracing=True,
  )

  # Define your remote and local dependencies separately
  remote_requirements = [
      # Add the essential package here
      "absl-py",
      "google-adk",
      "google-cloud-aiplatform",
      "google-genai",
      "pydantic",
      "python-dotenv",
      # Add the following if your agent's tools use them
      "requests",
      "diff-match-patch",
      "tabulate",
      "scikit-learn",

  ]

  local_packages = [
      AGENT_WHL_FILE_PATH
  ]

  remote_agent = agent_engines.create(
      adk_app,
      requirements=remote_requirements,
      extra_packages=local_packages,
      )



  print(f"Created remote agent: {remote_agent.resource_name}")



def delete(resource_id: str) -> None:
  remote_agent = agent_engines.get(resource_id)
  remote_agent.delete(force=True)
  print(f"Deleted remote agent: {resource_id}")


def main(argv: list[str]) -> None:  # pylint: disable=unused-argument

  load_dotenv(override=True)

  project_id = (
      FLAGS.project_id
      if FLAGS.project_id
      else os.getenv("GOOGLE_CLOUD_PROJECT")
  )
  location = (
      FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
  )
  bucket = (
      FLAGS.bucket
      if FLAGS.bucket
      else os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
  )

  print(f"PROJECT: {project_id}")
  print(f"LOCATION: {location}")
  print(f"BUCKET: {bucket}")

  if not project_id:
    print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
    return
  elif not location:
    print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
    return
  elif not bucket:
    print(
        "Missing required environment variable: GOOGLE_CLOUD_STORAGE_BUCKET"
    )
    return

  vertexai.init(
      project=project_id,
      location=location,
      staging_bucket=f"gs://{bucket}",
  )

  if FLAGS.create:
    create()
  elif FLAGS.delete:
    if not FLAGS.resource_id:
      print("resource_id is required for delete")
      return
    delete(FLAGS.resource_id)
  else:
    print("Unknown command")


if __name__ == "__main__":
  app.run(main)
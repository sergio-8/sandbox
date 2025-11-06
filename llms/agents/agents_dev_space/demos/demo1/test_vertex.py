# test_vertex.py
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "sv-ml-sandbox"
LOCATION = "us-central1"

print(f"Attempting to initialize Vertex AI for project '{PROJECT_ID}' in '{LOCATION}'...")

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print("Vertex AI initialized successfully.")

    print("\nFetching available models...")
    model = GenerativeModel("gemini-1.5-flash-latest")

    response = model.generate_content("Hi")

    print("\nSUCCESS! API call completed.")
    print("Response:", response.text)

except Exception as e:
    print("\n--- FAILED ---")
    print("An error occurred while trying to communicate with the Vertex AI API.")
    print("This confirms the issue is with the environment configuration, not the agent code.")
    print("\nError Details:")
    print(e)
    print("\n--- END OF REPORT ---")


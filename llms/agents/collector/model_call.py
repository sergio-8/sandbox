import vertexai
from vertexai.language_models import TextGenerationModel

# Replace with your actual project ID
PROJECT_ID ="bla bla bla "
LOCATION = "us-central1"

def get_hello_world_response(project_id: str, location: str) -> str:
    """Generates a simple 'Hello, World' style response using Vertex AI."""
    vertexai.init(project=project_id, location=location)
    # USE THE NEW MODEL NAME HERE:
    model = TextGenerationModel.from_pretrained("gemini-1.0-pro-002")

    prompt = "Say 'Hello, World!'"
    response = model.predict(prompt, max_output_tokens=25)

    return response.text

if __name__ == "__main__":
    response = get_hello_world_response(PROJECT_ID, LOCATION)
    print(f"Model Response: {response}")
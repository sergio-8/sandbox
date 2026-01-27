import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env")
        return
    
    print("Checking available models...")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for model in client.models.list():
            # Standard genai SDK models have a 'name' attribute
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()

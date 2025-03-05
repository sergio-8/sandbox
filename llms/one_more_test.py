# from google.generativeai import GenerativeModel, configure
# print("Import successful!")


import google.generativeai as genai
import os
from rich.markdown import Markdown
from rich import print



def ask_gemini_with_sdk(prompt, model_name="gemini-2.0-flash"):
    """
    Asks Gemini using the Google Generative AI Python SDK, retrieving the API key from an environment variable.

    Args:
        prompt: The prompt to send to Gemini.
        model_name: The name of the Gemini model to use.

    Returns:
        The generated text, or None if an error occurs.
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error: {e}")
        return None


# Example Usage:
prompt = "tell me about Supertubos, Portugal "
result = ask_gemini_with_sdk(prompt)

if result:
    markdown = Markdown(result)
    print(markdown)


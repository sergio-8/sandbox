import  google.generativeai




import GenerativeModel, configure

def ask_gemini_with_sdk(api_key, prompt, model_name="gemini-2.0-flash"):
    """
    Asks Gemini using the Google Generative AI Python SDK.

    Args:
        api_key: Your API key.
        prompt: The prompt to send to Gemini.
        model_name: The name of the Gemini model to use.

    Returns:
        The generated text, or None if an error occurs.
    """
    try:
        configure(api_key=api_key)
        model = GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None

api_key = "YOUR_VALID_API_KEY" #replace with your api key
prompt = "Explain quantum computing."
result = ask_gemini_with_sdk(api_key, prompt)

if result:
    print(result)

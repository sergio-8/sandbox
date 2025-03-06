import google.generativeai as genai

import os


# Get the value of the environment variable
variable_value = os.environ.get("GOOGLE_API_KEY")

# Check if the variable exists
if variable_value:
    print(f"Environment variable found: {variable_value}")
else:
    print("Environment variable not found.")



import os
from google.api_core import client_options as client_options_lib
from google.auth import credentials as ga_credentials
from google.cloud import generativelanguage_v1beta

# Set the environment variable for your API key
os.environ['GOOGLE_API_KEY'] = variable_value  # Replace with your actual API key

# Create a client with specifying the API key
client_options = client_options_lib.ClientOptions(
    api_key=os.environ.get('GOOGLE_API_KEY'),
)
client = generativelanguage_v1beta.TextServiceClient(client_options=client_options)

# Set the model name
model_name = "models/gemini-2.0-flash"

# Create the prompt
prompt = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works"
                }
            ]
        }
    ]
}

# Generate the content
response = client.generate_content(
    model=model_name,
    prompt=prompt
)

# Print the response
print(response.candidates[0].content)



"""

api_key = os.environ.get("GOOGLE_API_KEY")

if api_key:
    # Use the API key
    print("API Key found")
else:
    print("API Key - NOT - found")


genai.configure(api_key="GOOGLE_API_KEY")


flash = genai.GenerativeModel('gemini-1.5-flash')
response = flash.generate_content("Explain AI to me like I'm a kid.")
print(response.text)

#print(os.environ )

"""
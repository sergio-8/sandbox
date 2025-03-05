from google.generativeai import GenerativeModel, configure
from google-api-core import retry

import os
import google.generativeai as genai

from rich.markdown import Markdown
from rich import print


print("Import successful!")

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
"""
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

except Exception as e:
    print(f"Error: {e}")
"""

flash = genai.GenerativeModel('gemini-2.0-flash')
generation_config = genai.GenerationConfig(max_output_tokens=200)

short_one = genai.GenerativeModel('gemini-2.0-flash',generation_config = genai.GenerationConfig(max_output_tokens=100))


'''
chat = flash.start_chat(history=[])

response = chat.send_message(" well, HI,  my name is Bubbo!")

response1 = chat.send_message(" Do you remember what my name is???")

'''

response = short_one.generate_content('give a one hundred words essay on Supertubos, Portugal')
markdown = Markdown(response.text)
print(markdown)


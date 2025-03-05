from google.api_core import retry
from google.generativeai import GenerativeModel, configure


import os
import google.generativeai as genai

from rich.markdown import Markdown
from rich import print


print("Import successful!")
print("it worked")

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


response = short_one.generate_content('give a eighty words or less essay on what makes Jericho a special place ')
markdown = Markdown(response.text)
print(markdown)

'''


high_temp_model = genai.GenerativeModel(
    'gemini-2.0-flash',
    generation_config=genai.GenerationConfig(temperature=2.0))


# When running lots of queries, it's a good practice to use a retry policy so your code
# automatically retries when hitting Resource Exhausted (quota limit) errors.
retry_policy = {
    "retry": retry.Retry(predicate=retry.if_transient_error, initial=10, multiplier=1.5, timeout=300)
}

for _ in range(5):
  response = high_temp_model.generate_content('Pick a random colour... (respond in a single word)',
                                              request_options=retry_policy)
  if response.parts:
    print(response.text, '-' * 25)

print(" and now ... lowtemp same task....")

low_temp_model = genai.GenerativeModel(
    'gemini-2.0-flash',
    generation_config=genai.GenerationConfig(temperature=0.0))

for _ in range(5):
  response = low_temp_model.generate_content('Pick a random colour... (respond in a single word)',
                                             request_options=retry_policy)
  if response.parts:
    print(response.text, '-' * 25)



creative_model = genai.GenerativeModel(
    'gemini-2.0-flash',
    generation_config=genai.GenerationConfig(
        # These are the default values for gemini-1.5-flash-001.
        temperature=2.0,
        top_k=64,
        top_p=0.95,
    ))

story_prompt = "You are a creative writer. Write a fifty words story about a cat who goes on an adventure."
response = creative_model.generate_content(story_prompt, request_options=retry_policy)
print(response.text)
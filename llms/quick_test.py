from google.api_core import retry
from google.generativeai import GenerativeModel, configure
import enum
import typing_extensions as typing
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

classifier_model= genai.GenerativeModel(model_name="gemini-2.0-flash",
                                        generation_config=genai.GenerationConfig(
                                            temperature=0.1,
                                            top_k=1,
                                            max_output_tokens= 5,
                                        ))

zero_shot_prompt = """Classify movie reviews as POSITIVE, NEUTRAL or NEGATIVE.
Review: "Her" is a disturbing study revealing the direction
humanity is headed if AI is allowed to keep evolving,
unchecked. I wish there were so many more movies like this.
Sentiment: """

response_class = classifier_model.generate_content(zero_shot_prompt, request_options=retry_policy)
print("class_resp:" ,response_class.text)




class Sentiment(enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


model1 = genai.GenerativeModel(
    'gemini-1.5-flash-001',
    generation_config=genai.GenerationConfig(
        response_mime_type="text/x.enum",
        response_schema=Sentiment
    ))

response1 = model1.generate_content(zero_shot_prompt, request_options=retry_policy)
print(response1.text)


#----------------------------------------------------------------------------


class PizzaOrder(typing.TypedDict):
    size : str
    ingredients : list[str]
    type : str


json_model = genai.GenerativeModel(
    'gemini-1.5-flash-latest',
    generation_config=genai.GenerationConfig(
        temperature=0.1,
        response_mime_type="application/json",
        response_schema=PizzaOrder,
        top_p=1,
        max_output_tokens=250,
    ))



few_shot_prompt = """Parse a customer's pizza order into valid JSON:

EXAMPLE:
I want a small pizza with cheese, tomato sauce, and pepperoni.
JSON Response:
```
{
"size": "small",
"type": "normal",
"ingredients": ["cheese", "tomato sauce", "peperoni"]
}
```

EXAMPLE:
Can I get a large pizza with tomato sauce, basil and mozzarella
JSON Response:
```
{
"size": "large",
"type": "normal",
"ingredients": ["tomato sauce", "basil", "mozzarella"]
}

ORDER:
"""

customer_order = "Give me a large with cheese & pineapple"


json_response=json_model.generate_content([few_shot_prompt, customer_order],request_options = retry_policy)

json_response_1 = json_model.generate_content("Can I have a large dessert pizza with apple, icecream and chocolate")


print(json_response_1.text)



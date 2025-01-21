import os

import openai
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
    base_url="https://litellm.aks-hs-prod.int.hyperskill.org",
)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ]
)

print(response.choices[0].message.content)



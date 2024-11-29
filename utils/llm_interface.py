from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv() 

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def query_llm(prompt, model="claude-3-5-sonnet-latest"):
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
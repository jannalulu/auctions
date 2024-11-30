from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv() 

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def query_anthropic(prompt, model="claude-3-5-sonnet-latest"):
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def query_openai(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
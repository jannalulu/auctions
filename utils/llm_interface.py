from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv() 

anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
gemini_client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def query_anthropic(prompt, model="claude-3-5-sonnet-latest"):
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def query_openai(prompt, model="gpt-4o-mini"):
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def query_gemini(prompt, model="gemini-1.5-pro"):
    response = gemini_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
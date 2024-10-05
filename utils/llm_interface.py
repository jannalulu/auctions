from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def query_llm(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
"""hello_llm_py - Your first OpenAI API call.
Run it from the repo root:
python src/hello_llm.py "What is RAG in one sentence?"
"""

import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load OPEANAI_API_KEY from .env if a .env file exists.
load_dotenv()

#create an OpenAI clinet.
client = OpenAI()

def ask(question: str) -> str:
    """Send one question to the LLM and return the answer text."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are concise"},
            {"role": "user", "content": question},
        ],
        temperature=0.3
    )
    return resp.choices[0].message.content
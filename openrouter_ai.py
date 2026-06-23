from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def ask_ai(question, cpu, memory, network, risk):

    prompt = f"""
You are CloudGuard AI.

Current Metrics:
CPU: {cpu}%
Memory: {memory}%
Network: {network} KB
Risk: {risk}

User Question:
{question}

Provide a short cloud operations recommendation.
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
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

def cost_optimizer_ai(cpu, memory, network):

    prompt = f"""
You are a Cloud FinOps expert.

Current Infrastructure Metrics:
CPU: {cpu}%
Memory: {memory}%
Network: {network} KB

Analyze:
1. Whether the EC2 instance is overutilized or underutilized.
2. Cost optimization opportunities.
3. Estimated savings percentage.
4. Recommended AWS actions.

Keep the response short and practical.
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

def auto_remediation_ai(cpu, memory, network, risk):

    prompt = f"""
You are an AWS Cloud Operations Engineer.

Current Metrics:
CPU: {cpu}%
Memory: {memory}%
Network: {network} KB
Risk: {risk}

Generate:
1. Root Cause
2. Recovery Plan
3. AWS Services to Use
4. Estimated Recovery Time

Keep it short and actionable.
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
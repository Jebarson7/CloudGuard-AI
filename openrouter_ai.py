from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    api_key = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
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

def cost_optimizer_ai(cpu, memory, network, cost, cost_status):

    prompt = f"""
You are CloudGuard AI Cost Optimization Agent.

Facts (do not change these):

Monthly Cost: ${cost:.2f}
Cost Status: {cost_status}
CPU Usage: {cpu:.2f}%
Memory Usage: {memory}%
Network Usage: {network:.2f} KB

IMPORTANT:
These facts are already verified from AWS Cost Explorer.
Do NOT contradict them.
Do NOT mention increasing costs unless Cost Status is HAS_COST.

Your task is ONLY to provide recommendations.

Return exactly this format:

Recommendations:
• ...
• ...
• ...
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

def predictive_failure_ai(cpu, memory, network, status_check):

    prompt = f"""
You are an AWS Cloud Reliability Engineer.

Analyze these AWS CloudWatch metrics and predict if the infrastructure is likely to fail.

Metrics:
- CPU Usage: {cpu:.2f}%
- Memory Usage: {memory:.2f}%
- Network Usage: {network:.2f} KB
- EC2 Status Checks Failed: {status_check}

Your task:

1. Predict whether a failure is likely.
2. Estimate the failure probability (0-100%).
3. Predict the most likely failure.
4. Explain why.
5. Suggest preventive actions.

Return ONLY in this format:

Failure Probability:
Predicted Failure:
Severity:
Reason:
Recommendation:
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
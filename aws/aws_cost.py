import boto3
from datetime import date

try:
    # Local development (VS Code)
    from aws.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY
except ModuleNotFoundError:
    # Streamlit Cloud
    import streamlit as st

    AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]

cost_explorer = boto3.client(
    "ce",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="us-east-1"
)

def get_month_cost():

    today = date.today()

    first_day = today.replace(day=1)

    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            "Start": str(first_day),
            "End": str(today)
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]

    return round(float(amount), 2)

def get_cost_summary():

    today = date.today()

    first_day = today.replace(day=1)

    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            "Start": str(first_day),
            "End": str(today)
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    amount = float(
        response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    )

    estimated = response["ResultsByTime"][0]["Estimated"]

    return {
        "cost": max(0, round(amount, 2)),
        "estimated": estimated
    }

def get_cost_by_service():

    today = date.today()

    first_day = today.replace(day=1)

    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            "Start": str(first_day),
            "End": str(today)
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    services = []

    for group in response["ResultsByTime"][0]["Groups"]:

        service = group["Keys"][0]

        amount = float(
            group["Metrics"]["UnblendedCost"]["Amount"]
        )

        services.append({
            "service": service,
            "cost": max(0, round(amount, 2))
        })

    return sorted(
        services,
        key=lambda x: x["cost"],
        reverse=True
    )
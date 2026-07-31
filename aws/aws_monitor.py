import boto3
from datetime import datetime, timedelta

try:
    from aws.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, INSTANCE_ID
except ModuleNotFoundError:
    import streamlit as st

    AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
    AWS_REGION = st.secrets["AWS_REGION"]
    INSTANCE_ID = st.secrets["INSTANCE_ID"]

cloudwatch = boto3.client(
    "cloudwatch",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

response = cloudwatch.get_metric_statistics(
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[
        {
            "Name": "InstanceId",
            "Value": INSTANCE_ID
        }
    ],
    StartTime=datetime.utcnow() - timedelta(minutes=30),
    EndTime=datetime.utcnow(),
    Period=300,
    Statistics=["Average"]
)

if response["Datapoints"]:
    latest = sorted(
        response["Datapoints"],
        key=lambda x: x["Timestamp"]
    )[-1]

    print("CPU Usage:", round(latest["Average"], 2), "%")

else:
    print("No CPU data available yet.")
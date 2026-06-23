import boto3
from aws_config import *
from datetime import datetime, timedelta

INSTANCE_ID = "i-0865e8f3c43e17ad8"

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
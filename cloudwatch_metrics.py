import boto3
from datetime import datetime, timedelta
from aws_config import *

INSTANCE_ID = "i-0865e8f3c43e17ad8"

cloudwatch = boto3.client(
    "cloudwatch",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def get_cpu_usage():

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

        return round(latest["Average"], 2)

    return 0

def get_network_in():

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="NetworkIn",
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

    print(response["Datapoints"])

    if response["Datapoints"]:
        latest = sorted(
            response["Datapoints"],
            key=lambda x: x["Timestamp"]
        )[-1]

        return round(latest["Average"] / 1024, 2)

    return 0
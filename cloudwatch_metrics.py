import boto3
from datetime import datetime, timedelta
from aws_config import *

INSTANCE_ID = "i-0a281c83a51f3a6c4"

cloudwatch = boto3.client(
    "cloudwatch",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def get_metric(metric_name):

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
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

def get_cpu_usage():

    return get_metric("CPUUtilization")

def get_network_in():

    return round(
        get_metric("NetworkIn") / 1024,
        2
    )

def get_network_out():

    return round(
        get_metric("NetworkOut") / 1024,
        2
    )

def get_status_check():

    return get_metric("StatusCheckFailed")

def get_network_history():

    cloudwatch = boto3.client(
        "cloudwatch",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

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

    return sorted(
        response["Datapoints"],
        key=lambda x: x["Timestamp"]
    )

def get_cpu_history():

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

    return sorted(
        response["Datapoints"],
        key=lambda x: x["Timestamp"]
    )
import boto3
import streamlit as st

AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
AWS_REGION = st.secrets["AWS_REGION"]

cloudwatch = boto3.client(
    "cloudwatch",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


def create_cpu_alarm(instance_id, alarm_name, threshold):

    cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription="Created by CloudGuard AI",
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id
            }
        ],
        Statistic="Average",
        Period=300,
        EvaluationPeriods=2,
        Threshold=threshold,
        ComparisonOperator="GreaterThanThreshold",
        ActionsEnabled=False,
        Unit="Percent"
    )

def list_alarms():

    response = cloudwatch.describe_alarms()

    return response["MetricAlarms"]

def delete_alarm(alarm_name):

    cloudwatch.delete_alarms(
        AlarmNames=[alarm_name]
    )

def get_alarm_status():

    response = cloudwatch.describe_alarms()

    alarms = []

    for alarm in response["MetricAlarms"]:

        alarms.append({
            "name": alarm["AlarmName"],
            "state": alarm["StateValue"],
            "reason": alarm["StateReason"],
            "updated": alarm["StateUpdatedTimestamp"]
        })

    return alarms
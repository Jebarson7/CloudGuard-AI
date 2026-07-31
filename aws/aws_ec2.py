import boto3
import time

try:
    # Local development (VS Code)
    from aws.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
except ModuleNotFoundError:
    # Streamlit Cloud
    import streamlit as st

    AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
    AWS_REGION = st.secrets["AWS_REGION"]

ec2 = boto3.client(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def list_instances():

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]

            name = instance_id

            if "Tags" in instance:

                for tag in instance["Tags"]:

                    if tag["Key"] == "Name":
                        name = tag["Value"]

            instances.append(
                {
                    "name": name,
                    "id": instance_id
                }
            )

    return instances


def get_instance_status(instance_id):
    response = ec2.describe_instances(
        InstanceIds=[instance_id]
    )

    return response["Reservations"][0]["Instances"][0]["State"]["Name"]


def start_instance(instance_id):
    ec2.start_instances(
        InstanceIds=[instance_id]
    )


def stop_instance(instance_id):
    ec2.stop_instances(
        InstanceIds=[instance_id]
    )


def reboot_instance(instance_id):
    ec2.reboot_instances(
        InstanceIds=[instance_id]
    )

def restart_instance(instance_id):

    stop_instance(instance_id)

    waiter = ec2.get_waiter("instance_stopped")

    waiter.wait(
        InstanceIds=[instance_id]
    )

    start_instance(instance_id)

def get_instance_details(instance_id):

    response = ec2.describe_instances(
        InstanceIds=[instance_id]
    )

    instance = response["Reservations"][0]["Instances"][0]

    name = "N/A"

    if "Tags" in instance:

        for tag in instance["Tags"]:

            if tag["Key"] == "Name":
                name = tag["Value"]

    return {

        "Name": name,

        "InstanceId": instance["InstanceId"],

        "State": instance["State"]["Name"],

        "InstanceType": instance["InstanceType"],

        "PublicIP": instance.get("PublicIpAddress", "N/A"),

        "LaunchTime": instance["LaunchTime"],

        "Region": AWS_REGION

    }
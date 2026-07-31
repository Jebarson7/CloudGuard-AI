import boto3
from aws.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

ec2 = boto3.client(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

response = ec2.describe_instances()

print("✅ Connected to AWS successfully!")

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print("Instance ID:", instance["InstanceId"])
        print("State:", instance["State"]["Name"])
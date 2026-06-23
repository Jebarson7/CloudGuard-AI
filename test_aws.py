import boto3
from aws_config import *

cloudwatch = boto3.client(
    "cloudwatch",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

print("AWS Connected Successfully")
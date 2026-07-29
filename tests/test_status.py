from aws_ec2 import get_instance_status

INSTANCE_ID = "i-0a281c83a51f3a6c4"

print(get_instance_status(INSTANCE_ID))
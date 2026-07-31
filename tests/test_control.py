from aws.aws_ec2 import stop_instance

INSTANCE_ID = "i-0a281c83a51f3a6c4"

stop_instance(INSTANCE_ID)

print("Stop command sent successfully.")
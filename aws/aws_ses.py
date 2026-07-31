import boto3

try:
    # Local development (VS Code)
    from aws.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
except ModuleNotFoundError:
    # Streamlit Cloud
    import streamlit as st

    AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
    AWS_REGION = st.secrets["AWS_REGION"]

ses = boto3.client(
    "ses",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


def send_email(receiver, subject, body):

    response = ses.send_email(

        Source="jebarson696@gmail.com",

        Destination={
            "ToAddresses": [
                receiver
            ]
        },

        Message={

            "Subject": {
                "Data": subject
            },

            "Body": {
                "Text": {
                    "Data": body
                }
            }

        }

    )

    return response
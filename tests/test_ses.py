from aws.aws_ses import send_email

response = send_email(

    receiver="jebarson696@gmail.com",

    subject="CloudGuard AI Test",

    body="""
CloudGuard AI Notification

Amazon SES is working successfully!

Congratulations!
"""

)

print(response)
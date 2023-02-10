import json
import urllib.parse
import boto3


# Function based on documentation:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-sending-receiving-msgs.html


print('Loading function')
sqs = boto3.client('sqs')
queue_url = "${queue_url}"


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    if 'body' in event:
        message = str(json.loads(str(event['body'])))
    elif 'queryStringParameters' in event:
        message = str(event['queryStringParameters'])
    else:
        message = "empty message"

    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Deployment': {
                'DataType': 'String',
                'StringValue': 'Terraform'
            },
            'Language': {
                'DataType': 'String',
                'StringValue': 'Python'
            },
            'Version': {
                'DataType': 'Number',
                'StringValue': '1'
            },
            'ARN': {
                'DataType': 'String',
                'StringValue': context.invoked_function_arn
            },
            'RequestID': {
                'DataType': 'String',
                'StringValue': context.aws_request_id
            },
            'Message': {
                'DataType': 'String',
                'StringValue': message
            },
        },
        MessageBody=(
            message
        )
    )

    print("Send SQS message: " + response['MessageId'])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "RequestID ": context.aws_request_id,
            "ReceivedMessage": message
        })
    }

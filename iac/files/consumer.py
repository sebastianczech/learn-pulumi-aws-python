import json
import boto3
import ast


print('Loading function')
sns = boto3.client('sns')
dynamodb = boto3.client('dynamodb')
topic_url = "Calling __str__ on an Output[T] is not supported.

To get the value of an Output[T] as an Output[str] consider:
1. o.apply(lambda v: f"prefix{v}suffix")

See https://pulumi.io/help/outputs for more details.
This function may throw in a future version of Pulumi."
table_url = "Calling __str__ on an Output[T] is not supported.

To get the value of an Output[T] as an Output[str] consider:
1. o.apply(lambda v: f"prefix{v}suffix")

See https://pulumi.io/help/outputs for more details.
This function may throw in a future version of Pulumi."


def lambda_handler(event, context):
    for record in event['Records']:
        payload = record["body"].replace("'",'"')
        print("Received SQS message: " + payload)
        data = json.loads(payload)
        print("Converted data: " + str(data))

        if "message" in data and "key" in data:
            item = dynamodb.put_item(
                TableName=table_url,
                Item=
                {
                    'ID': {
                        'S': str(data["key"]),
                    },
                    'message': {
                        'S': str(data["message"]),
                    }
                }
            )
            print("Insert item into DynamoDB: " + item['ResponseMetadata']['RequestId'])

        if "transport" in data and data["transport"] == "mail":
            subject = "Message from SQS"
            response = sns.publish(
                TopicArn=topic_url,
                Message=str(payload),
                Subject=subject,
            )
            print("Send SNS event: " + response['MessageId'])
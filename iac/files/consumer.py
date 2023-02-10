import json
import boto3
import ast


print('Loading function')
sns = boto3.client('sns')
dynamodb = boto3.client('dynamodb')
topic_url = "${topic_url}"
table_url = "${table_url}"


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

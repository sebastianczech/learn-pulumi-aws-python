import json

import pulumi as pulumi
from pulumi_aws import sqs, sns, dynamodb, iam, lambda_

# Create SQS queue: https://www.pulumi.com/registry/packages/aws/api-docs/sqs/queue/
pulumi_sqs_serverless_rest_api = sqs.Queue("pulumi_sqs_serverless_rest_api",
                                           fifo_queue=False,
                                           tags={
                                               "Environment": "development",
                                               "Name": "pulumi_sqs_serverless_rest_api",
                                           })

# Create SNS topic: https://www.pulumi.com/registry/packages/aws/api-docs/sns/topic/
pulumi_sns_serverless_rest_api = sns.Topic("pulumi_sns_serverless_rest_api",
                                           tags={
                                               "Environment": "development",
                                               "Name": "pulumi_sns_serverless_rest_api",
                                           })

# Create SNS topic subscription: https://www.pulumi.com/registry/packages/aws/api-docs/sns/topicsubscription/
pulumi_sns_topic_email_subscription = sns.TopicSubscription("pulumi_sns_topic_email_subscription",
                                                            topic=pulumi_sns_serverless_rest_api.arn,
                                                            protocol="email",
                                                            endpoint="sebaczech@gmail.com")

# Create DynamoDB table: https://www.pulumi.com/registry/packages/aws/api-docs/dynamodb/table/
pulumi_dynamodb_serverless_rest_api = dynamodb.Table("pulumi_dynamodb_serverless_rest_api",
                                                     attributes=[
                                                         dynamodb.TableAttributeArgs(
                                                             name="ID",
                                                             type="S",
                                                         ),
                                                     ],
                                                     hash_key="ID",
                                                     tags={
                                                         "Environment": "development",
                                                         "Name": "pulumi_dynamodb_serverless_rest_api",
                                                     },
                                                     read_capacity=20,
                                                     write_capacity=20)

# TODO: prepare ZIP file with Python code for:
#  - consumer
#  - producer

# TODO: create 3 IAM policies for consumer:
#  - lambda_consumer_sqs_receive_iam_policy
#  - lambda_consumer_sns_publish_iam_policy
#  - lambda_consumer_dynamo_put_iam_policy

# TODO: create event source mapping for consumer

# TODO: create Lambda endpoint (function URL) with Lambda permission for producer

# TODO: create cloud watch log group with IAM policy for:
#  - consumer
#  - producer

# Create IAM policy: https://www.pulumi.com/registry/packages/aws/api-docs/iam/policy/
pulumi_lambda_producer_sqs_send_iam_policy = iam.Policy("pulumi_lambda_producer_sqs_send_iam_policy",
                                                        path="/",
                                                        description="IAM policy for Lambda producer & SQS",
                                                        policy=pulumi_sqs_serverless_rest_api.arn.apply(
                                                            lambda x: json.dumps({
                                                                "Version": "2012-10-17",
                                                                "Statement": [
                                                                    {
                                                                        "Sid": "ProducerStatement",
                                                                        "Action": [
                                                                            "sqs:SendMessage"
                                                                        ],
                                                                        "Effect": "Allow",
                                                                        "Resource": x
                                                                    }
                                                                ]
                                                            })))

# Create IAM role: https://www.pulumi.com/registry/packages/aws/api-docs/iam/role/
pulumi_iam_for_lambda_producer = iam.Role("pulumi_lambda_producer_role", assume_role_policy="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
""")

# Create IAM role policy attachment: https://www.pulumi.com/registry/packages/aws/api-docs/iam/rolepolicyattachment/
pulumi_lambda_producer_sqs = iam.RolePolicyAttachment("pulumi_lambda_producer_sqs",
                                                      role=pulumi_iam_for_lambda_producer.name,
                                                      policy_arn=pulumi_lambda_producer_sqs_send_iam_policy.arn)

# Create Lambda: https://www.pulumi.com/registry/packages/aws/api-docs/lambda/function/
pulumi_lambda_producer = lambda_.Function("pulumi_lambda_producer",
                                          code=pulumi.FileArchive("files/producer.zip"),
                                          role=pulumi_iam_for_lambda_producer.arn,
                                          handler="producer.lambda_handler",
                                          runtime="python3.9",
                                          environment=lambda_.FunctionEnvironmentArgs(
                                              variables={
                                                  "foo": "bar",
                                              },
                                          ))

# Create IAM policy: https://www.pulumi.com/registry/packages/aws/api-docs/iam/policy/
pulumi_lambda_consumer_sqs_receive_iam_policy = iam.Policy("pulumi_lambda_consumer_sqs_receive_iam_policy",
                                                           path="/",
                                                           description="IAM policy for Lambda consumer & SQS",
                                                           policy=pulumi_sqs_serverless_rest_api.arn.apply(
                                                               lambda x: json.dumps({
                                                                   "Version": "2012-10-17",
                                                                   "Statement": [
                                                                       {
                                                                           "Sid": "ConsumerStatementSqs",
                                                                           "Action": [
                                                                               "sqs:ReceiveMessage",
                                                                               "sqs:DeleteMessage",
                                                                               "sqs:GetQueueAttributes"
                                                                           ],
                                                                           "Effect": "Allow",
                                                                           "Resource": x
                                                                       }
                                                                   ]
                                                               })))

pulumi_lambda_consumer_sns_publish_iam_policy = iam.Policy("pulumi_lambda_consumer_sns_publish_iam_policy",
                                                           path="/",
                                                           description="IAM policy for Lambda consumer & SNS",
                                                           policy=pulumi_sns_serverless_rest_api.arn.apply(
                                                               lambda x: json.dumps({
                                                                   "Version": "2012-10-17",
                                                                   "Statement": [
                                                                       {
                                                                           "Sid": "ConsumerStatementSns",
                                                                           "Action": [
                                                                               "sns:Publish"
                                                                           ],
                                                                           "Effect": "Allow",
                                                                           "Resource": x
                                                                       }
                                                                   ]
                                                               })))

pulumi_lambda_consumer_dynamo_put_iam_policy = iam.Policy("pulumi_lambda_consumer_dynamo_put_iam_policy",
                                                          path="/",
                                                          description="IAM policy for Lambda consumer & DynamoDB",
                                                          policy=pulumi_dynamodb_serverless_rest_api.arn.apply(
                                                              lambda x: json.dumps({
                                                                  "Version": "2012-10-17",
                                                                  "Statement": [
                                                                      {
                                                                          "Sid": "ConsumerStatementDynamoDb",
                                                                          "Action": [
                                                                              "dynamodb:PutItem"
                                                                          ],
                                                                          "Effect": "Allow",
                                                                          "Resource": x
                                                                      }
                                                                  ]
                                                              })))

# Create IAM role: https://www.pulumi.com/registry/packages/aws/api-docs/iam/role/
pulumi_iam_for_lambda_consumer = iam.Role("pulumi_lambda_consumer_role", assume_role_policy="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
""")

# Create IAM role policy attachment: https://www.pulumi.com/registry/packages/aws/api-docs/iam/rolepolicyattachment/
pulumi_lambda_consumer_sqs = iam.RolePolicyAttachment("pulumi_lambda_consumer_sqs",
                                                      role=pulumi_iam_for_lambda_consumer.name,
                                                      policy_arn=pulumi_lambda_consumer_sqs_receive_iam_policy.arn)

pulumi_lambda_consumer_sns = iam.RolePolicyAttachment("pulumi_lambda_consumer_sns",
                                                      role=pulumi_iam_for_lambda_consumer.name,
                                                      policy_arn=pulumi_lambda_consumer_sns_publish_iam_policy.arn)

pulumi_lambda_consumer_dynamodb = iam.RolePolicyAttachment("pulumi_lambda_consumer_dynamodb",
                                                           role=pulumi_iam_for_lambda_consumer.name,
                                                           policy_arn=pulumi_lambda_consumer_dynamo_put_iam_policy.arn)

# Create Lambda: https://www.pulumi.com/registry/packages/aws/api-docs/lambda/function/
pulumi_lambda_consumer = lambda_.Function("pulumi_lambda_consumer",
                                          code=pulumi.FileArchive("files/consumer.zip"),
                                          role=pulumi_iam_for_lambda_consumer.arn,
                                          handler="consumer.lambda_handler",
                                          runtime="python3.9",
                                          environment=lambda_.FunctionEnvironmentArgs(
                                              variables={
                                                  "foo": "bar",
                                              },
                                          ))

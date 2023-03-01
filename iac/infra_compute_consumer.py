import json

import pulumi as pulumi
from jinja2 import Environment, FileSystemLoader
from pulumi_aws import iam, lambda_, cloudwatch

from infra_database import pulumi_dynamodb_serverless_rest_api
from infra_integration import pulumi_sqs_serverless_rest_api, pulumi_sns_serverless_rest_api

# TODO: resolve issue with getting ID of resource as string

# Get Jinja2 template and render Python script
environment = Environment(loader=FileSystemLoader("files/"))
template = environment.get_template("consumer.jinja2")
content = template.render(
    topic_url=pulumi_sns_serverless_rest_api.id.apply(lambda v: f"{v}"),
    table_url=pulumi_dynamodb_serverless_rest_api.id.apply(lambda v: f"{v}")
)
with open("files/consumer.py", mode="w", encoding="utf-8") as rendered:
    rendered.write(content)

# TODO: prepare ZIP file with Jinja template for Python code for:
#  - consumer

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

pulumi_lambda_iam_consumer_logging = iam.Policy("pulumi_lambda_iam_consumer_logging",
                                                path="/",
                                                description="IAM policy for Lambda consumer & CloudWatch logs",
                                                policy=json.dumps({
                                                    "Version": "2012-10-17",
                                                    "Statement": [
                                                        {
                                                            "Action": [
                                                                "logs:CreateLogGroup",
                                                                "logs:CreateLogStream",
                                                                "logs:PutLogEvents"
                                                            ],
                                                            "Resource": "arn:aws:logs:*:*:*",
                                                            "Effect": "Allow"
                                                        }
                                                    ]
                                                }))

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

pulumi_lambda_consumer_logs = iam.RolePolicyAttachment("pulumi_lambda_consumer_logs",
                                                       role=pulumi_iam_for_lambda_consumer.name,
                                                       policy_arn=pulumi_lambda_iam_consumer_logging.arn)

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

# Create CloudWatch log groups: https://www.pulumi.com/registry/packages/aws/api-docs/cloudwatch/loggroup/
pulumi_lambda_producer_log_group = cloudwatch.LogGroup("/aws/lambda/pulumi_lambda_producer_log_group",
                                                       retention_in_days=1,
                                                       tags={
                                                           "Environment": "development",
                                                           "Name": "pulumi_lambda_producer_log_group",
                                                       })

pulumi_lambda_consumer_log_group = cloudwatch.LogGroup("/aws/lambda/pulumi_lambda_consumer_log_group",
                                                       retention_in_days=1,
                                                       tags={
                                                           "Environment": "development",
                                                           "Name": "pulumi_lambda_consumer_log_group",
                                                       })

# Create Lambda event source mapping: https://www.pulumi.com/registry/packages/aws/api-docs/lambda/eventsourcemapping/
pulumi_event_source_mapping_sqs_lambda_consumer = lambda_.EventSourceMapping(
    "pulumi_event_source_mapping_sqs_lambda_consumer",
    event_source_arn=pulumi_sqs_serverless_rest_api.arn,
    function_name=pulumi_lambda_consumer.arn)

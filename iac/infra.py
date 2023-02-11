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

# TODO: provision Lambda - producer

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

# TODO: provision Lambda - consumer

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

pulumi_lambda_consumer = lambda_.Function("pulumi_lambda_consumer",
                                          code=pulumi.FileArchive("files/consumer.zip"),
                                          role=pulumi_iam_for_lambda_producer.arn,
                                          handler="consumer.lambda_handler",
                                          runtime="python3.9",
                                          environment=lambda_.FunctionEnvironmentArgs(
                                              variables={
                                                  "foo": "bar",
                                              },
                                          ))
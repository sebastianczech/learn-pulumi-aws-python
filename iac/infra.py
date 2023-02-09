from pulumi_aws import sqs, sns, dynamodb

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

# TODO: provision Lambda - consumer

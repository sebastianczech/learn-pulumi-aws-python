from pulumi_aws import sqs, sns

# Create SQS: https://www.pulumi.com/registry/packages/aws/api-docs/sqs/queue/
pulumi_sqs_serverless_rest_api = sqs.Queue("pulumi_sqs_serverless_rest_api",
                                           fifo_queue=False,
                                           tags={
                                               "Environment": "development",
                                           })

# Create SNS: https://www.pulumi.com/registry/packages/aws/api-docs/sns/topic/
pulumi_sns_serverless_rest_api = sns.Topic("pulumi_sns_serverless_rest_api")

# Create SNS topic subscription: https://www.pulumi.com/registry/packages/aws/api-docs/sns/topicsubscription/
pulumi_sns_topic_email_subscription = sns.TopicSubscription("pulumi_sns_topic_email_subscription",
                                                            topic=pulumi_sns_serverless_rest_api.arn,
                                                            protocol="email",
                                                            endpoint="sebaczech@gmail.com")

# TODO: provision DynamoDB

# TODO: provision Lambda - producer

# TODO: provision Lambda - consumer

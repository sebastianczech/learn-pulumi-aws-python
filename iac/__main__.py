import pulumi

import infra

pulumi.export('pulumi_sqs_serverless_rest_api', infra.pulumi_sqs_serverless_rest_api.arn)
pulumi.export('pulumi_sns_serverless_rest_api', infra.pulumi_sns_serverless_rest_api.arn)
pulumi.export('pulumi_sns_topic_email_subscription', infra.pulumi_sns_topic_email_subscription.arn)
pulumi.export('pulumi_dynamodb_serverless_rest_api', infra.pulumi_dynamodb_serverless_rest_api.arn)
pulumi.export('pulumi_lambda_producer', infra.pulumi_lambda_producer.arn)
pulumi.export('pulumi_lambda_consumer', infra.pulumi_lambda_consumer.arn)

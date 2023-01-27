import pulumi

import infra

pulumi.export('pulumi_sqs_serverless_rest_api', infra.pulumi_sqs_serverless_rest_api.arn)
pulumi.export('pulumi_sns_serverless_rest_api', infra.pulumi_sns_serverless_rest_api.arn)
pulumi.export('pulumi_sns_topic_email_subscription', infra.pulumi_sns_topic_email_subscription.arn)

# TODO: export DynamoDB

# TODO: export Lambda - producer

# TODO: export Lambda - consumer

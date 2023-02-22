import pulumi

import infra_database, infra_integration, infra_compute_consumer, infra_compute_producer

pulumi.export('pulumi_sqs_serverless_rest_api', infra_integration.pulumi_sqs_serverless_rest_api.arn)
pulumi.export('pulumi_sns_serverless_rest_api', infra_integration.pulumi_sns_serverless_rest_api.arn)
pulumi.export('pulumi_sns_topic_email_subscription', infra_integration.pulumi_sns_topic_email_subscription.arn)
pulumi.export('pulumi_dynamodb_serverless_rest_api', infra_database.pulumi_dynamodb_serverless_rest_api.arn)
pulumi.export('pulumi_lambda_producer', infra_compute_producer.pulumi_lambda_producer.arn)
pulumi.export('pulumi_lambda_consumer', infra_compute_consumer.pulumi_lambda_consumer.arn)

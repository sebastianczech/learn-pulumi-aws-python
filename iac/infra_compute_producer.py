import json

import pulumi as pulumi
from jinja2 import Environment, FileSystemLoader
from pulumi_aws import iam, lambda_, sqs

from infra_integration import pulumi_sqs_serverless_rest_api

# Get Jinja2 template and render Python script
environment = Environment(loader=FileSystemLoader("files/"))
template = environment.get_template("producer.jinja2")
content = template.render(
    queue_url=sqs.get_queue(name=pulumi_sqs_serverless_rest_api.name).id
)
with open("files/producer.py", mode="w", encoding="utf-8") as rendered:
    rendered.write(content)

# TODO: prepare ZIP file with Jinja template for Python code for:
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

pulumi_lambda_iam_producer_logging = iam.Policy("pulumi_lambda_iam_producer_logging",
                                                path="/",
                                                description="IAM policy for Lambda producer & CloudWatch logs",
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

pulumi_lambda_producer_logs = iam.RolePolicyAttachment("pulumi_lambda_producer_logs",
                                                       role=pulumi_iam_for_lambda_producer.name,
                                                       policy_arn=pulumi_lambda_iam_producer_logging.arn)

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

# Create Lambda function URL: https://www.pulumi.com/registry/packages/aws/api-docs/lambda/functionurl/
pulumi_lambda_producer_endpoint = lambda_.FunctionUrl("pulumi_lambda_producer_endpoint",
                                                      function_name=pulumi_lambda_producer.name,
                                                      authorization_type="AWS_IAM",
                                                      cors=lambda_.FunctionUrlCorsArgs(
                                                          allow_credentials=True,
                                                          allow_origins=["*"],
                                                          allow_methods=["*"],
                                                          allow_headers=[
                                                              "date",
                                                              "keep-alive",
                                                          ],
                                                          expose_headers=[
                                                              "keep-alive",
                                                              "date",
                                                          ],
                                                          max_age=86400,
                                                      ))

# Get user: https://www.pulumi.com/registry/packages/aws/api-docs/iam/getuser/
iam_user_seba = iam.get_user(user_name="seba")

# Create Lambda permission: https://www.pulumi.com/registry/packages/aws/api-docs/lambda/permission/
allow_iam_user = lambda_.Permission("AllowExecutionForIamUser",
                                    action="lambda:InvokeFunctionUrl",
                                    function=pulumi_lambda_producer.name,
                                    principal=iam_user_seba.arn,
                                    function_url_auth_type="AWS_IAM"
                                    )

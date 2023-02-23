from pulumi_aws import dynamodb

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
                                                     read_capacity=1,
                                                     write_capacity=1)

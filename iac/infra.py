import pulumi
from pulumi_aws import sqs

# Create an AWS resource (SQS)
queue = sqs.Queue("learn_pulumi_sqs",
    fifo_queue=False,
    tags={
        "Environment": "development",
    })

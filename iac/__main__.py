"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import sqs

# Create an AWS resource (SQS)
queue = sqs.Queue("learn_pulumi_sqs",
    fifo_queue=False)

# Export the name of the queue
pulumi.export('queue_arn', queue.arn)

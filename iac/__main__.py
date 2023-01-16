import pulumi

import infra

# Export the name of the queue
pulumi.export('queue_arn', infra.queue.arn)

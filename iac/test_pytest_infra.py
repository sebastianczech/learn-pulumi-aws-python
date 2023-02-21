import pulumi


class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + '_id', args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(
    MyMocks(),
    preview=False,  # Sets the flag `dry_run`, which is true at runtime during a preview.
)

# It's important to import `infra` _after_ the mocks are defined.
import infra


def check_tags(args):
    urn, tags = args
    assert tags is not None
    assert "Environment" in tags
    assert "Name" in tags


@pulumi.runtime.test
def test_queue_has_tag_name():
    return pulumi.Output.all(infra.pulumi_sqs_serverless_rest_api.urn,
                             infra.pulumi_sqs_serverless_rest_api.tags).apply(check_tags)


@pulumi.runtime.test
def test_topic_has_tag_name():
    return pulumi.Output.all(infra.pulumi_sns_serverless_rest_api.urn,
                             infra.pulumi_sns_serverless_rest_api.tags).apply(check_tags)


@pulumi.runtime.test
def test_dynamodb_has_tag_name():
    return pulumi.Output.all(infra.pulumi_dynamodb_serverless_rest_api.urn,
                             infra.pulumi_dynamodb_serverless_rest_api.tags).apply(check_tags)

# TODO: test Lambda with all components for:
#  - producer
#  - consumer

# TODO: split tests into multiple files

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


@pulumi.runtime.test
def test_queue_has_tag_name():
    def check_tags(args):
        urn, tags = args
        assert tags is not None
        assert "Environment" in tags

    return pulumi.Output.all(infra.pulumi_sqs_serverless_rest_api.urn, infra.pulumi_sqs_serverless_rest_api.tags).apply(
        check_tags)

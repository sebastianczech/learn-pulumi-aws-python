import pytest
import pulumi
import infra

class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + '_id', args.inputs]
    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}

pulumi.runtime.set_mocks(
    MyMocks(),
    preview=False,  # Sets the flag `dry_run`, which is true at runtime during a preview.
)

@pulumi.runtime.test
def test_queue_has_tag_name():
    def check_tags(args):
        urn, tags = args
        assert tags is not None
        assert "Name" in tags

    return pulumi.Output.all(infra.queue.urn, infra.queue.tags).apply(check_tags)

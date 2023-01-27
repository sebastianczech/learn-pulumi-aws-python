import unittest
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

class TestingWithMocks(unittest.TestCase):
    @pulumi.runtime.test
    def test_queue_tags(self):
        def check_tags(args):
            urn, tags = args
            self.assertIsNotNone(tags, f'queue {urn} must have tags')
            self.assertIn('Environment', tags, f'queue {urn} must have a name tag')

        return pulumi.Output.all(infra.queue.urn, infra.queue.tags).apply(check_tags)
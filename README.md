# Learn Pulumi - deploy infrastructure into AWS cloud using Python

Repository was created while learning Pulumi and doing [getting started](https://www.pulumi.com/docs/get-started/aws/) for AWS and Python. 

## Quickstart

In order to start work with Pulumi, new project was created using commands:
```bash
mkdir iac
cd iac
pulumi new aws-python -s sebastianczech/learn-pulumi-aws-python/dev
```

In order to use always free services from [AWS Free Tier](https://aws.amazon.com/free), I modified Python code delivered from template to add SQS queue. 

Next step was to preview changes, deploy them and destroy infrastructure:

```bash
pulumi preview
pulumi up --yes
pulumi destroy --yes
```

## Testing

As infrastructure code is written in Python, it can be easily test as presented in [example unit tests](https://github.com/pulumi/examples/tree/master/testing-unit-py).

```
pytest
```

## Other

TODO - [workspace on GitPod](https://gitpod.io/workspaces).


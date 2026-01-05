#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from cdk_provisioning.iam_stack import IAMStack
from cdk_provisioning.server_stack import ServerStack
# from cdk_provisioning.database_stack import DatabaseStack

aws_env = cdk.Environment(account=os.getenv("AWS_ACCOUNT_ID"), region='us-east-2')

app = cdk.App()
# IAMStack(app, "IAMStack", env=aws_env)
ServerStack(app, "ServerStack", env=aws_env)
# DatabaseStack(app, "DatabaseStack", env=aws_env)

app.synth()

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_provisioning.server_stack import ServerStack

aws_env = cdk.Environment(account=cdk.Aws.ACCOUNT_ID, region='us-east-2')

app = cdk.App()

server = ServerStack(
    scope = app, 
    construct_id = "ServerStack", 
    env = aws_env
)

app.synth()

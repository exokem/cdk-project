#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_provisioning.app_stack import AppStack
from cdk_provisioning.server_stack import ServerStack
from cdk_provisioning.provisioning_stack import ProvisioningStack

aws_env = cdk.Environment(account=cdk.Aws.ACCOUNT_ID, region='us-east-2')

app = cdk.App()

main = AppStack(
	scope = app,
	construct_id = "AppStack",
	env = aws_env
)

server = ServerStack(
    scope = app, 
    construct_id = "ServerStack", 
	event_bus = main.event_bus,
    env = aws_env
)

provisioning = ProvisioningStack(
	scope = app,
	construct_id = "ProvisioningStack",
	event_bus = main.event_bus,
	env = aws_env
)

app.synth()

from typing import List
from aws_cdk import (
    Stack,
	RemovalPolicy,
    
	aws_lambda as _lambda,

	aws_iam as _iam,

	aws_logs as _logs,

	aws_events as _events,
	aws_events_targets as _targets,
)
from constructs import Construct
import os

class ProvisioningStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, event_bus: _events.EventBus, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		log_group = _logs.LogGroup(
			scope = self,
			id = "ProvisioningStackLogGroup",
			retention=_logs.RetentionDays.ONE_DAY,

			removal_policy = RemovalPolicy.DESTROY
		)

		provisioning_code = _lambda.Code.from_asset(
			os.path.join(os.path.dirname(__file__), "lambda/provisioning")
		)

		provision_stack_lambda = _lambda.Function(
			scope = self,
			id = "ProvisionStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.provision_stack",
			code = provisioning_code,
			log_group = log_group,
		)

		event_bus.grant_all_put_events(provision_stack_lambda)

		provision_stack_rule = _events.Rule(
			scope = self,
			id = "OnCreateProvisionStackRule",
			event_bus = event_bus,
			event_pattern = _events.EventPattern(
				source=["handlers.create_stack"]
			),
		)

		provision_stack_rule.add_target(_targets.LambdaFunction(provision_stack_lambda))

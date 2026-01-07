from typing import List
from aws_cdk import (
    Stack,
	RemovalPolicy,
    
	aws_dynamodb as _dynamo,
	aws_lambda as _lambda,

    aws_apigatewayv2 as _apigateway,
    aws_apigateway as _apigateway_old,
    aws_apigatewayv2_integrations as _integrations,
    aws_apigatewayv2_authorizers as _authorizers,
	aws_iam as _iam,

	aws_logs as _logs,

	aws_events as _events,
	aws_events_targets as _targets,
)
from constructs import Construct
import os

class AppStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

### EVENTBRIDGE ###

		event_bus = _events.EventBus(
			scope = self,
			id = "AppEventBus",
			event_bus_name = "AppEventBus"
		)

		self.event_bus = event_bus
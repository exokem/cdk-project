from typing import List
from aws_cdk import (
    Stack,
    
	aws_iam as _iam,
)
from constructs import Construct

class IAMStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

# Provision Amplify Access to API Gateway
		# api_access_role = _iam.Role(
		# 	scope = self,
		# 	id = "AmplifyApiAccessRole",
		# 	assumed_by = _iam.ServicePrincipal("amplify.amazonaws.com"),

		# 	managed_policies = [
		# 		_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess")
		# 	]
		# )

# Provision Lambda Access to DynamoDB
		self.lambda_dynamo_access_role = _iam.Role(
			scope = self,
			id = "LambdaDatabaseAccessRole",
			assumed_by = _iam.ServicePrincipal("lambda.amazonaws.com"),

			managed_policies = [
				_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess_v2")
			]
		)
from typing import List
from aws_cdk import (
    Stack,
    
	aws_lambda as _lambda,

    aws_apigatewayv2 as _apigateway,
    aws_apigatewayv2_integrations as _integrations,
    aws_apigatewayv2_authorizers as _authorizers,
    
	aws_iam as _iam,
)
from constructs import Construct
import os

class ServerStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

### LAMBDA ###

		stack_code = _lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "lambda/stack"))

### API GATEWAY ###

		api = _apigateway.HttpApi(
			scope = self,
			id = "MetaDeploymentGateway",

			cors_preflight = _apigateway.CorsPreflightOptions(
				allow_headers = ["Authorization"],
				allow_methods = [
					_apigateway.CorsHttpMethod.POST,
					_apigateway.CorsHttpMethod.GET,
					_apigateway.CorsHttpMethod.PATCH,
					_apigateway.CorsHttpMethod.DELETE,
				],
				allow_origins = ["*"], # TBD -- restrict to amplify
			),

			# Authorize with IAM
			# default_authorizer = _authorizers.HttpIamAuthorizer(),
		)

		routes: List[_apigateway.HttpRoute] = []

# Create (Deploy) Stack
		create_stack_lambda = _lambda.Function(
			scope = self,
			id = "CreateStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.create_stack",
			code = stack_code
		)

		routes.extend(api.add_routes(
			path = "/stack/{name}",
			methods = [_apigateway.HttpMethod.POST],
			integration = _integrations.HttpLambdaIntegration("CreateStackIntegration", create_stack_lambda),
		))
		
# Read Stack
		read_stack_lambda = _lambda.Function(
			scope = self,
			id = "ReadStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.read_stack",
			code = stack_code
		)

		routes.extend(api.add_routes(
			path = "/stack/{id}",
			methods = [_apigateway.HttpMethod.GET],
			integration = _integrations.HttpLambdaIntegration("ReadStackIntegration", read_stack_lambda),
		))

# Update (Redeploy) Stack
		update_stack_lambda = _lambda.Function(
			scope = self,
			id = "UpdateStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.update_stack",
			code = stack_code
		)

		routes.extend(api.add_routes(
			path = "/stack/{id}",
			methods = [_apigateway.HttpMethod.PATCH],
			integration = _integrations.HttpLambdaIntegration("ReadStackIntegration", update_stack_lambda),
		))

# Destroy Stack
		destroy_stack_lambda = _lambda.Function(
			scope = self,
			id = "DestroyStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.destroy_stack",
			code = stack_code
		)

		routes.extend(api.add_routes(
			path = "/stack/{id}",
			methods = [_apigateway.HttpMethod.DELETE],
			integration = _integrations.HttpLambdaIntegration("DestroyStackIntegration", destroy_stack_lambda),
		))

# API Auth
		# for route in routes:
		# 	# route.grant_invoke(_iam.AnyPrincipal())
		# route.grant_invoke(api_access_role)

# Publish API
		_apigateway.HttpStage(
			scope = self,
			id = "MetaDeploymentGatewayMainStage",
			stage_name = "dev",

			http_api = api,
		)
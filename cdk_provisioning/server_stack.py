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
)
from constructs import Construct
import os

class ServerStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		table_name = "Stacks"

### CLOUDWATCH ###

		log_group = _logs.LogGroup(
			scope = self,
			id = "ServerStackLogGroup",
			retention=_logs.RetentionDays.ONE_DAY,

			removal_policy = RemovalPolicy.DESTROY
		)

### DYNAMODB ###

		db = _dynamo.TableV2(
			scope = self,
			id = "StackReferenceTable",

			table_name = table_name,
			table_class = _dynamo.TableClass.STANDARD,

			partition_key = _dynamo.Attribute(
				name = "stack",
				type = _dynamo.AttributeType.STRING,
			),

			# Ensure database is destroyed (should not do this in production)
			removal_policy = RemovalPolicy.DESTROY,
		)

### LAMBDA ###

		stack_code = _lambda.Code.from_asset(
			os.path.join(os.path.dirname(__file__), "lambda/stack")
		)

		lambda_env = {
			"TABLE_NAME": table_name
		}

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

# Create (Deploy) Stack
		create_stack_lambda = _lambda.Function(
			scope = self,
			id = "CreateStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.create_stack",
			code = stack_code,
			environment = lambda_env,
			log_group = log_group
		)

		db.grant(create_stack_lambda, "dynamodb:PutItem", "dynamodb:GetItem")

		create_stack_routes = api.add_routes(
			path = "/stack",
			methods = [_apigateway.HttpMethod.POST],
			integration = _integrations.HttpLambdaIntegration("CreateStackIntegration", create_stack_lambda)
		)

# Read Stack
		read_stack_lambda = _lambda.Function(
			scope = self,
			id = "ReadStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.read_stack",
			code = stack_code,
			environment = lambda_env,
			log_group = log_group
		)

		db.grant(read_stack_lambda, "dynamodb:GetItem")

		read_stack_routes = api.add_routes(
			path = "/stack/{name}",
			methods = [_apigateway.HttpMethod.GET],
			integration = _integrations.HttpLambdaIntegration("ReadStackIntegration", read_stack_lambda)
		)

# Update (Redeploy) Stack
		update_stack_lambda = _lambda.Function(
			scope = self,
			id = "UpdateStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.update_stack",
			code = stack_code,
			environment = lambda_env,
			log_group = log_group
		)
		
		db.grant(update_stack_lambda, "dynamodb:UpdateItem", "dynamodb:GetItem")

		update_stack_routes = api.add_routes(
			path = "/stack",
			methods = [_apigateway.HttpMethod.PATCH],
			integration = _integrations.HttpLambdaIntegration("ReadStackIntegration", update_stack_lambda)
		)

# Destroy Stack
		destroy_stack_lambda = _lambda.Function(
			scope = self,
			id = "DestroyStackFunction",

			runtime = _lambda.Runtime.PYTHON_3_12,
			handler = "handlers.destroy_stack",
			code = stack_code,
			environment = lambda_env,
			log_group = log_group
		)

		db.grant(destroy_stack_lambda, "dynamodb:DeleteItem", "dynamodb:GetItem")

		destroy_stack_routes = api.add_routes(
			path = "/stack/{name}",
			methods = [_apigateway.HttpMethod.DELETE],
			integration = _integrations.HttpLambdaIntegration("DestroyStackIntegration", destroy_stack_lambda)
		)

# Publish API
		# _apigateway.CfnStage(
		# 	scope = self,
		# 	id = "MetaDeploymentGatewayMainStage",
		# 	stage_name = "dev",

		# 	api_id = api.api_id,

		# 	access_log_settings = _apigateway.CfnStage.AccessLogSettingsProperty(
		# 		destination_arn = log_group.log_group_arn,
		# 		format = _apigateway_old.AccessLogFormat.clf().to_string()
		# 	)
		# )

		
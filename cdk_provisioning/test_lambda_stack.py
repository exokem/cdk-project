from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput
)
from constructs import Construct


class TestLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        example_lambda = _lambda.Function(
            # This stack instance is the parent of the lambda function
            scope = self,
            # Lambda name
            id = "ExampleLambdaFunction",

            # Node runtime version
            runtime = _lambda.Runtime.NODEJS_20_X,

            # Function code
            # TODO: how else can we define the code???
            handler = "index.handler",
            code = _lambda.Code.from_inline(
                """
                exports.handler = async function(event) {
                    return {
                        statusCode: 200,
                        body: JSON.stringify('Hello World!'),
                    };
                };
                """
            )
        )

        function_url = example_lambda.add_function_url(
            # Public endpoint - no auth
            auth_type = _lambda.FunctionUrlAuthType.NONE
        )

        CfnOutput(self, "exampleFunctionUrlOutput", value=function_url.url)

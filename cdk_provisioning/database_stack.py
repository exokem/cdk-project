from typing import List
from aws_cdk import (
    Stack,
    
	aws_iam as _iam,
	aws_dynamodb as _dynamo,
)
from constructs import Construct
import os

class DatabaseStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		db = _dynamo.TableV2(
			scope = self,
			id = "StackReferenceTable",

			table_name = "Stacks",
			table_class = _dynamo.TableClass.STANDARD,

			partition_key = ""
		)

		


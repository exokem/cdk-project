from typing import List
from aws_cdk import (
    Stack,
	RemovalPolicy,

	aws_s3 as _s3,
	aws_s3_deployment as _s3deploy,
    
	aws_iam as _iam,

	aws_logs as _logs,

	aws_events as _events,
	aws_events_targets as _targets,
)
from constructs import Construct
import os

class ClientStack(Stack):
    
	def __init__(self, scope: Construct, construct_id: str, api_url: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

### S3 ###

		bucket = _s3.Bucket(
			scope = self,
			id = "ClientPageBucket",
			block_public_access = _s3.BlockPublicAccess.BLOCK_ACLS_ONLY,
			website_index_document = "index.html",
			public_read_access = True,
			auto_delete_objects = True,
			removal_policy = RemovalPolicy.DESTROY,
		)

		html = ""

		with open(os.path.join(os.path.dirname(__file__), "client/index.html"), "r") as index:
			html = index.read()

		deployment = _s3deploy.BucketDeployment(
			scope = self,
			id = "ClientPageDeployment",
			sources = [
				_s3deploy.Source.data(
					object_key = "index.html",
					data = html.replace("#API_URL#", api_url)
				)
				# _s3deploy.Source.asset(os.path.join(os.path.dirname(__file__), "client"))
			],
			destination_bucket = bucket,
		)

		print(bucket.bucket_website_url)

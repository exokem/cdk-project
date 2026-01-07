import json
import boto3
import os
import datetime
import logging

events = boto3.client("events")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def provision_stack(event, context):

	detail = event.get("detail")

	events.put_events(
        Entries=[
            {
                "Source": "provisioning.provision_stack",
                "EventBusName": "AppEventBus",
                
				"Detail": json.dumps({
                    "stack": detail.get("stack")
				}),
                "DetailType": "JSON"
            }
        ]
    )
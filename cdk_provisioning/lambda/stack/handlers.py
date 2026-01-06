import json
import boto3
import os
import datetime
import logging

table_name: str = os.getenv("TABLE_NAME")
client = boto3.client("dynamodb")
db = boto3.resource("dynamodb")
table = db.Table(table_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def extract_body(event) -> dict:
    body = event.get("body")

    if body is None:
        return {}

    return json.loads(body)


def extract_params(event) -> dict:
    params = event.get("pathParameters")

    if params is None:
        return {}

    return params


def create_stack(event, context):
    body = extract_body(event)

    # Stack to deploy
    stack = body.get("stack")

    check = table.get_item(
        Key={
            "stack": stack
        }
    )

    if check.get("Item") is not None:
        logger.info(f"Skipping request to deploy stack '{stack}': The requested stack has already been deployed.")
        return {
            "statusCode": 409,
            "body": "The requested stack has already been deployed."
        }

    time = str(datetime.datetime.now())

    table.put_item(
        Item={
            "stack": stack,
            "state": "deploying",
            "date_created": time,
            "date_updated": time
        }
    )

    # TODO: eventbridge -- trigger deployment action
    # TODO: after deployment completes, update state to "active"

    return {
        'statusCode': 202,
        'body': "Stack deployment initiated."
    }


def read_stack(event, context):
    params = extract_params(event)
    
    stack = params.get("name")

    if stack is None:
        logger.info(f"Skipping request to query stack '{stack}': The requested stack name is not valid.")
        return {
            "statusCode": 400,
            "body": "The request did not identify a valid stack."
        }

    result = table.get_item(
        Key={
            "stack": stack
        }
    )

    data = result.get("Item")

    if data is None:
        return {
            "statusCode": 404,
            "body": "The requested stack does not exist."
        }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }


def update_stack(event, context):
    body = extract_body(event)

    stack = body.get("stack")

    if stack is None:
        return {
            "statusCode": 400,
            "body": "The request did not identify a valid stack."
        }

    check = table.get_item(
        Key={
            "stack": stack,
        }
    )

    data = check.get("Item")

    if data is None:
        return {
            "statusCode": 404,
            "body": "The requested stack does not exist."
        }

    # if data.get("state") == "deploying":
    #     return {
    #         "statusCode": 409,
    #         "body": "The requested stack is busy."
    #     }

    table.update_item(
        Key={
            "stack": stack
        },
        UpdateExpression="SET #s = :new_status, date_updated = :new_date_updated",
        ExpressionAttributeNames={
            "#s": "state"
        },
        ExpressionAttributeValues={
            ":new_status": "deploying",
            ":new_date_updated": str(datetime.datetime.now())
        }
    )

    # TODO: eventBridge action to trigger redeploy

    return {
        "statusCode": 202,
        "body": "Stack update initiated."
    }

    

def destroy_stack(event, context):
    params = extract_params(event)
    
    stack = params.get("name")

    if stack is None:
        return {
            "statusCode": 400,
            "body": "The request did not identify a valid stack."
        }

    result = table.get_item(
        Key={
            "stack": stack
        }
    )

    data = result.get("Item")

    if data is None:
        return {
            "statusCode": 404,
            "body": "The requested stack does not exist."
        }

    # if data.get("state") == "deploying":
    #     return {
    #         "statusCode": 409,
    #         "body": "The requested stack is busy."
    #     }

    table.delete_item(
        Key={
            "stack": stack
        }
    )

    # TODO: eventbridge deletion

    return {
        "statusCode": 202,
        "body": "Stack deletion initiated."
    }
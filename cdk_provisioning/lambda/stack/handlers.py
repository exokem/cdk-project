import json

def create_stack(event, context):
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('POST stack')
	}

def read_stack(event, context):
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('GET status')
    }

def update_stack(event, context):
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps("PATCH stack")
	}

def destroy_stack(event, context):
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps("DELETE stack")
	}
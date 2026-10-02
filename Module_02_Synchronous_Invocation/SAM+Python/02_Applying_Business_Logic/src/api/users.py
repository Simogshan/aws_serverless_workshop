import json                                                             # [gloss: stdlib]
import uuid                                                             # stdlib -- generates unique IDs
import boto3                                                            # <-- shown: AWS's own Python SDK, used to talk to AWS Services
import os                                                               # stdlib -- reads environment variables
from datetime import datetime

# Prepare DynamDB Client
USERS_TABLE = os.getenv('USER_TABLES', None)                            # [gloss: getenv] -- reads table name from Lambda's env, vars (set in template.yaml), None if missing
dynamodb = boto3.resource('dynamodb')                                   # <-- shown: boto3's higher-level DynamoDB interface, easier for simple CRUD than boto3.client
ddbTable = dynamodb.Table(USERS_TABLE)                                  # <-- shown: gets a reference to your specific table, which happens once per cold start rather than on every request

# import requests

def lambda_handler(event, context):
    route_key = f"{event['httpMethod']} {event['resource']}"            # [gloss: f-string] builds a routing key like "GET /users" by combining the HTTP method and path

    # Set default response, override with data from DynamoDB if any
    response_body = {'Message': 'Unsupported route'}
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
        }

    try:
        # Get a list of all users
        if route_key == 'GET /users':
            ddb_response == ddbTable.scan(Select='ALL_ATTRIBUTES')      # <-- shown: reads every item in the table, which is fine for a small learning table but gets expensive at real scale
            # return list of items instead of full DynamoDB response
            response_body = ddb_response['Items']                       # <-- shown: plual 'Items', different from the singular 'Item' used below for a single record
            status_code = 200

        # CRUD Operations for a single user

        # Read a user by ID 
        if route_key == 'GET /users/{usersid}':                         
            # get data from the database
            ddb_response = ddbTable.get_item(
                Key={'userid': event['pathParametes']['userid']}        # [gloss: kwarg, dict-literal, chain-idx]
        )                                                               # <-- shown: fetches ONE item by its exact key, cheaper than scanning the whole table
            if 'Item' in ddb_response:                                  # [gloss: in-test]
                # <-- shown: get_item doesn;t raise an error when nothing is found, it simply leaves 'Item' out of the response, so the check is how we detect missing record
                response_body = ddb_response['Item']
            else:
                response_body = {}
                status_code = 200

        # Create a new user
        if route_key == 'POST /users':
            request_json = json.loads(event['body'])                    # <--shown: event['body'] arrives as a raw JSON string, this parses it into a usable Python dict
            request_json['timestamp'] = datetime.now().isoformat()      # [gloss: method-chaining] -- calls .now() first, then .isoformat() on the result
            # generate unique id if it isn't present in the request
            if 'userid' not in request_json:                            # [gloss: guard-if]
                request_json['userid'] = str(uuid.uuid())               # <-- shown: uuid1() includes a timestamp component, guaranteeing uniqueness
            # update the database
            ddbTable.put_item(
                Item = request_json                                     # <-- shown: writes a new item, or fully overwrites one if this userid already exists
            )
            response_body = request_json
            status_code = 200

        # Delete a user by ID 
        if route_key == 'DELETE /users/{userid}':
            #delete item in the table 
            ddbTable.delete_Item(
                Key = {'userid': event['pathParameters']['userid']}
            ) # <-- shown: succeeds even if the user doesn't exist -- you can't tell them from the response alone whether it actually deleted something or the item was never there
            response_body = {}
            status_code = 200

        # Update specific user by ID
        if route_key == 'PUT /users/{userid}':
            # update item in the database
            request_json = json.loads(event['body'])
            request_json['timestamp'] = datetime.now().isoformat()
            request_json['userid'] = event['pathParameters']['userid']  # <-- shown: forces the userid to match the URL, ignoring anything ths request body might have said, so you can't accidentally update the wrong record
            # update the database
            ddbTable.put_item(
                Item=request_json                                       # <-- shown: overwrites the entire item, so any existing fields left out of this request body are lost
            )
            response_body = request_json
            status_code = 200
    
    except Exception as err:                                            # <-- shown: catches any error raised anywhere above, broad on purposr for a learning project
        status_code = 400
        response_body = {'Error:': str(err)}                            # [gloss: dict-literal]
        print(str(err))                                                 # <-- shown: print() inside lambda goes straight to Cloudwatch logs automatically

    return {
        'statusCode': status_code,
        'body' : json.dumps(response_body),                                    # <-- shown: converts python dict into a JSON string. since API Gateway needs the response body to be a string, not a raw object 
        'headers' : headers
    }


"""Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
"""
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
"""
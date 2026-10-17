import json                                                             # [gloss: stdlib]
import uuid                                                             # [gloss: stdlib] -- generates unique IDs
import boto3                                                            # <-- shown: AWS's own Python SDK, used to talk to AWS Services
import os                                                               # [gloss: stdlib] -- reads environment variables
from datetime import datetime                                           # [gloss: stdlib]

# Prepare DynamoDB Client
USERS_TABLE = os.getenv('USER_TABLES', None)                            # [gloss: getenv] -- reads table name from Lambda's environment variables (set in template.yaml), None if missing
dynamodb = boto3.resource('dynamodb')                                   # <-- shown: boto3's higher-level DynamoDB interface, easier for simple CRUD than boto3.client
ddbTable = dynamodb.Table(USERS_TABLE)                                  # <-- shown: gets a reference to your specific table, which happens once per cold start rather than on every request

# import requests

def lambda_handler(event, context):                                     # [gloss: handler]
    route_key = f"{event['httpMethod']} {event['resource']}"            # [gloss: f-string, dict-index] builds a routing key like "GET /users" by combining the HTTP method and path

    # Set default response, override with data from DynamoDB if any
    response_body = {'Message': 'Unsupported route'}                    #  <-- shown: this is the fallback answer, used only if none of the route checks below match
    status_code = 400                                                   # <-- shown: fallback status, also only used if nothing below changes it
    headers = {
        'Content-Type': 'application/json',                             # <-- shown: tells the caller the response body is JSON
        'Access-Control-Allow-Origin': '*'                              # <-- shown: lets any website call this API from a browser, not just one specific site
        }

    try:
        # Get a list of all users
        if route_key == 'GET /users':
            ddb_response = ddbTable.scan(Select='ALL_ATTRIBUTES')      # <-- shown: reads every items in the table, which is fine for a small learning table but gets expensive at real scale
            # return list of items instead of full DynamoDB response
            response_body = ddb_response['Items']                       # <-- shown: plual 'Items', different from the singular 'Item' used below for a single record
            status_code = 200

        # CRUD Operations for a single user

        # Read a user by ID 
        if route_key == 'GET /users/{userid}':                         
            # get data from the database
            ddb_response = ddbTable.get_item(
                Key={'userid': event['pathParameters']['userid']}     # [gloss: kwarg, dict-literal, chain-idx]
        )                                                               # <-- shown: fetches ONE item by its exact key, cheaper than scanning the whole table
            if 'Item' in ddb_response:                                  # [gloss: in-test]
                # <-- shown: get_item doesn't raise an error when nothing is found, it simply leaves 'Item' out of the response, so this check is how we detect a missing record
                response_body = ddb_response['Item']
            else:
                response_body = {}
            status_code = 200

        # Create a new user
        if route_key == 'POST /users':
            request_json = json.loads(event['body'])                    # <-- shown: event['body'] arrives as a raw JSON string, this parses it into a usable Python dict
            request_json['timestamp'] = datetime.now().isoformat()      # [gloss: dict-assign, method-chaining] -- calls .now() first, then .isoformat() on the result
            # generate unique id if it isn't present in the request
            if 'userid' not in request_json:                            # [gloss: guard-if]
                request_json['userid'] = str(uuid.uuid1())              # [gloss: uuid] <-- shown: uuid1() includes a timestamp component, guaranteeing uniqueness
            # update the database
            ddbTable.put_item(
                Item = request_json                                     # <-- shown: writes a new item, or fully overwrites one if this userid already exists
            )
            response_body = request_json
            status_code = 200

        # Delete a user by ID 
        if route_key == 'DELETE /users/{userid}':
            # delete item in the table 
            ddbTable.delete_item(
                Key = {'userid': event['pathParameters']['userid']}
            ) # <-- shown: succeeds even if the user doesn't exist -- you can't tell from the response alone whether it actually deleted something or the item was never there
            response_body = {}
            status_code = 200

        # Update specific user by ID
        if route_key == 'PUT /users/{userid}':
            # update item in the database
            request_json = json.loads(event['body'])                    # [gloss: json]
            request_json['timestamp'] = datetime.now().isoformat()
            request_json['userid'] = event['pathParameters']['userid']  # <-- shown: forces the userid to match the URL, ignoring anything this request body might have said, so you can't accidentally update the wrong record
            # update the database
            ddbTable.put_item(
                Item=request_json                                       # <-- shown: overwrites the entire item, so any existing fields left out of this request body are lost
            )
            response_body = request_json
            status_code = 200
    
    except Exception as err:                                            # [gloss: exception] <-- shown: catches any error raised anywhere above, broad on purpose for a learning project
        status_code = 400
        response_body = {'Error:': str(err)}                            # [gloss: dict-literal]
        print(str(err))                                                 # [gloss: str-cast] <-- shown: print() inside Lambda goes straight to Cloudwatch logs automatically

    return {
        'statusCode': status_code,
        'body' : json.dumps(response_body),                             # [gloss: json] <-- shown: converts Python dict into a JSON string. since API Gateway needs the response body to be a string, not a raw object 
        'headers' : headers                                             # <-- shown: closes out the return dict, sending the headers set above back with the response
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
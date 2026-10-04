## Trace: GET /users/{userid}

1. Request arrives: event['httpMethod']='GET', event['resource']='/users/{userid}'
2. route_key = "GET /users/{userid}"
3. response_body/status_code set to defaults (unused so far)
4. Enter try block
5. Check route_key == 'GET /users'? No -- skip
6. Check route_key == 'GET /users/{userid}'? YES -- enter this block
7. Call get_item with the userid pulled from the URL path
8. AWS returns a response -- check if 'Item' key exists in it
9. If found: response_body = the actual item. If not: response_body = {}
10. status_code = 200
11. Skip DELETE, POST, PUT blocks entirely -- remaining if Checked and is False
12. No exception raised -- skip except block
13. Return {statusCode: 200, body: json string of the item, headers}

## Trace: GET /users

1. Request arrives: event['httpMethod'] = 'GET', event['resource'] = '/users'
2. route_key = "GET /users"
3. response_body/status_code set to defaults(unused so far)
4. Enter try block
5. Check route_key == 'GET /users'? Yes -- enter this block
6. Call scan to scan (Select='all attribute') 
7. Items from the dynamodb table will list all content in response_body
8 status_code = 200
9. Skip GET / {usersid}, DELETE, PUT, POST blocks entirely -- each remaining if checked and is false
10. No exception raised -- skip except block
11. Return {statusCode: 200, body: json string of the items, headers}

## Trace: Post /users

1. Request arrives: event['httpMethod'] = 'POST', event['resource'] = '/users'
2. route_key = "POST /users"
3. response_body/status_code set to defaults
4. Enter try block
5. Check route_key == 'GET /users'? No -- skip
6. Check route_key == 'GET /users/{userid}'? No -- skip
7. Check route_key == 'POST /users'? Yes -- enter this block
8. request_json what is happening here json raw strings into python object
9. request_json['timestamp'] creating new key named timestamp to add current date and time with isoformat 
10. Check If 'userid' Key exist in it
11. IF found: key -> unchanged, If not: created Key with a new generated with unique-id
12. Call put_item to create new item or replaces the old item with a new item in the table, if primary key (userid) already exist
13. response_body is updated to current request_json
14. status_code = 200
15. Skip DELETE, PUT block entirely -- remaining if Checked and is False
16. No exception raised -- skip except block
17. Return {statusCode: 200, body: json string of the item, headers}

## Trace PUT /users/{userid}

1. Request arrived: event['httpMethod'] = 'PUT', event['resource'] = '/users/{userid}'
2. route_key = "PUT /users/{userid}"
3. response_body/status_code set to defaults
4. Enter try block
5. Check route_key == 'GET /users'? No -- skip
6. Check route_key == 'GET /users/{userid}'? No -- skip
7. Check route_key == 'POST /users/'? No -- skip
8. Check route_key == 'DELETE /users/{userid}'? No -- skip
9. Check route_key == 'PUT /users/{userid}'? Yes -- enter this block
10. Convert JSON RAW strings into python object by calling json.loads
11. Creating new key named timestamp to add current date and time wiht isoformat for update
12. request_json['userid'] -> calling userid from the URL path 
13. call put_item to replace the old item to new / updated item with the exisiting userid
14. response_body is updated to current request_json
15. status_code = 200
16. route_key == 'PUT' request is last in the file, So there's nothing left to skip
17. No exception raised -- skip except block
18. Return {statusCode: 200, body: json string of the item, headers}

## Trace Exception 

1. Request arrived: event['httpMethod'] = 'PUT', event['resource'] = '/users/{userid}'
2. route_key = "PUT /users/{userid}"
3. response_body/status_code set to defaults
4. Enter try block
5. Check route_key == 'GET /users'? No -- skip
6. Check route_key == 'GET /users/{userid}'? No -- skip
7. Check route_key == 'POST /users/'? No -- skip
8. Check route_key == 'DELETE /users/{userid}'? No -- skip
9. Check route_key == 'PUT /users/{userid}'? Yes -- enter this block
10. Called json.loads but failed due to invalid json  "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)\" 
11. Rest of try block does not run
12. exception catches it, err holds the JSONDecodeError object
13. status code = 400
14. exception raised -- Expecting property name enclosed in double quotes
15. Return ```{  "statusCode": 400,
  "body": "{\"Error:\": \"Expecting property name enclosed in double quotes: line 1 column 2 (char 1)\"}",
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  }
}```  
Exception raise error if something happened in code syntax, runtime errors, client request error

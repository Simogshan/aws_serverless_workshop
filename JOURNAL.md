# Serverless-Workshop

## Module 01 : Intro to Serverless : September 06,2026

## Part 01: Start with Data

### What I Learned
- Created user table in dynamodb using AWS Console
- Created a new lambda function with existing basic python code from scratch using AWS Console 
- Created Test Event to test the function
- Learned the outputs of Function logs such as Start, Latest, End, Report, Request ID
- Changed the code from a lambda function, redeploy the code and tested the function and worked through the resulting errors

### Errors

1. Error: "Syntax error in module 'lambda_function': invalid syntax. Perhaps you forgot a comma?
   ErrorType: "Runtime.UserCodeSyntaxError"
   Cause: 'body': json.dumps(line_item, sort_keys=True)
   Fix: Added comma at the end of the code

2. Error: "Object of type LambdaContext is not JSON serializable"
   ErrorType: "TypeError"
   Cause: 'body':json.dumps(context)
   Fix: Context cannot be mapped into json like event. Note: kinda explored what will happen

3. Error: "'LambdaContext' object has no attribute 'color'",
   ErrorType: "AttributeError"
   Cause: 'body':json.dumps(context.color)
   Fix: Again still try to understand "context"

## Part 02: Connect to DynamoDB

### What I Learned 
- Created a python function to connect existing table in dynamodb from lambda
- Added some users with  primary key in python lambda function 
- deployed the code and test the function and we got error, here we learned about giving / accessing permissions to the services
- From lambda function, gave permissions to dynamodb services by attach policies 

### Errors

1. Error: "name 'persom' is not defined"
   ErrorType: "NameError"
   Cause: format(persom[\"userid\"])
   Fix: corrected persom into person

2. Error: "An error occurred (AccessDeniedException) when calling the BatchWriteItem operation
   ErrorType: "ClientError"
   Cause: no identity-based policy allows the dynamodb:BatchWriteItem action
   Fix: Added Permission to Dynamodb from lambda function. Note: Error happened intentionally

3. Error: "An error occurred (ValidationException) when calling the BatchWriteItem operation: The provided key element does not match the schema"
   ErrorType: "ClientError"
   Cause: primary key name from dynamodb is different from lambda primary key name
   Fix: Corrected the name

## Part 03: Build an API

### What I Learned
- API creates an entry point to access lambda function to return data here such as user data
- Created lambda function to get user data from dynamodb, later we will access via API gateway 
- Created permission from lambda function limit access from Dynamodb called DynamoDBreadonly access. hence name implies can read data only 
- Created REST API in API Gateway via the AWS Console -- set up the resource and method, then tested and deployed it

### Error

*Didn't encountered Errors during the API Gateway session -- everything was done through the console and the code was simple.
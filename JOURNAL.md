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

---

## Module 02: Synchronous Invocation : September 14, 2026

### What I Learned
- In larger projects, we need many more resources and have to provision infrastructure for many developers and environments such as dev, stage, prod
- Web-based console is easy and broad, but it will slow you down and make you prone to mistakes
- We are going to use *Infrastructure as Code (IaC)* to define, deploy and test service resource and code
- Client wants to migrate exisiting framework to serverless. As a first step we move our operation to monolithic, or mono-lambda function.
- Here we are going to use a mono-lambda function, which contains the entire application logic and routes to incoming events because it may be easy to understand what is happening internally. 

## Part 01 : SAM + Python

### What I Learned
- AWS CloudFormation is a form of IaC, CFN templates are written in YAML or JSON 
- __AWS Serverless Application Model (AWS SAM)__ templates declare infrastructure resources, such as functions, APIs and databases.
- When AWS SAM templates are used to provision infrastructure, they are first transformed into  CFN Templates
- If you define __Transform: AWS::Serverless-2016-10-31__ in CFN template automatically considered as SAM Template

`Note: The AWS Workshop provide files and folders for the project structure`

### Section 01 : Create Data Store

### What I Learned
- Created a table in DynamoDB using AWS SAM CFN Template 
- __Resources__ Section is very important in Cloudformation Template because it's the only thing mandatory to build the infrastructure
- Learned about __Intrinsic Function__, it means built-in function to assign values to properties that are not available until runtime. here used !Sub called __substitute__

### Commands

1. __sam build__ : processes your AWS SAM template file

2. __sam validate__ : validates your AWS SAM template YAML content

3. __sam deploy --guided --stack-name example__ : deploys the project after building it, --guided used for first time per region. this mode shows the parameter required for deployment, provides default option, and save them

4. __sam delete --stack-name example__: deletes entire project along with permissions, stacks from CFN, other services

### Error

1. Error: Globals, It must be a non-empty dictionary  
   ErrorType:InvalidGlobalsSectionException   
   Cause: Globals: -> section in template.yaml file  
   ErrorHappenedAt: During sam build command  
   Fix: Commented Global Section, because it wasn't needed for this build  

2. Error: Failed to create changeset for the stack: ws-serverless-patterns-users,  
   ErrorType:ValidationError  
   Cause: `- AttributeName: userid  - AttributeType: S`  
   ErrorHappenedAt: During sam build command  
   Fix: Removed extra - from AttributeType because __-__ consider Array in YAML

3. Error: Failed to create/update the stack: ws-serverless-patterns-users,  
   ErrorType:ValidationError  
   Cause: KeyType: Hash  
   ErrorHappenedAt: During sam deploy command  
   Fix: Hash should be Caps HASH

4. Note: Indentation matters in YAML.
   


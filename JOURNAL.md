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
   
### Section 02 : Add Business Logic : September 20, 2026 - October 05, 2026

### What I Learned
- Created a Lambda function connected to the existing Dynamodb Usertable template, which has now become version 2
- Created a Python file containing business logic: GetUser, DeleteUser, AddUser, GetUserById, UpdateUserById  
**The code itself**  
   - Created GET user to list all user items from the table. For short table its cheap but for the table contains more data, SCAN properties going to costs more and takes longer
   - Created GET user by User ID, to retrieve a specific user's item from the list 
   - Created New User by POST method, to create a user item in the table -- if no ID is provided in the request,a userID is automatically generated
   - Created PUT user by user ID to update a specific user's item
   - Created Delete user to delete the item from the table
- Encountered a handful of bugs during build, deploy and in invoke
- Created a learning method to study the code and template  
**The Learning Method (TAG)**
   - Reading the code is different from writing the code
   - __Trace__: Created to study the flow of Python code, how the block of code works
   - __Annotation__: Created to explain what a specific line is actually doing, used in both CFN Templates & Python code
   - __Glossary__: Created to learn Python syntax, with examples and results for each   
- Created and add dependencies in requirement file 

### Errors

1. Error: invalid syntax (users.py, line 18)  
   ErrorType: Runtime.UserCodeSyntaxError  
   Cause: response_body == {'Message': 'Unsupported route'}  
   ErrorHappenedAt: During Lambda Test Invoke  
   ErrorPhase: Before/Init -- never reached handler  
   Fix: response_body = {'Message': 'Unsupported route'} 

2. Error: unindent does not match any outer indentation level (users.py, line 100)  
   ErrorType: IndentationError  
   Cause:  """Sample pure  
   ErrorHappenedAt: During Lambda Test Invoke  
   ErrorPhase: Before/Init -- never reached handler  
   Fix: """Sample pure - fixed indentation

3. Error: Required parameter name not set   
   ErrorType: ValueError  
   Cause:  USERS_TABLE - Environment variable not matched  
   ErrorHappenedAt: During Lambda Test Invoke  
   ErrorPhase: Before/Init -- never reached handler  
   Fix: USER_TABLES

4. Error: 'httpMehod'     
   ErrorType: KeyError  
   Cause:  test event JSON was missing the 'httpMethod' key, so event ['httpMethod'] on line 16 had nothing to find  
   ErrorHappenedAt: During Lambda Test Invoke  
   ErrorPhase: Runtime -- Uncaught (route_key sits outside the try block, so except never gets a chance to catch this)  
   Fix: corrected the test event JSON to include httpMethod

5. Error: "name 'ddbtable' is not defined"  
   ErrorType:ValidationError  
   Cause: ddtable  
   ErrorHappenedAt: During Lambda Test Event Invoke  
   ErrorPhase: After/Runtime -- caught by except  
   Fix: Renamed ddtable into ddTable

6. Error: "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"  
   ErrorType: JSONDecodeError  
   Cause: "body": "{invalid json"  
   ErrorHappenedAt: During Lambda Test Event Invoke  
   ErrorPhase:  After/Runtime -- caught by except  
   Fix: "body": "{invalid json}"  
   ```Note: This error is intentionally made to check test event to see what kind of error makes for to note trace excepton```

7. Error: module 'uuid' has no attribute 'uuid'  
   ErrorType: AttributeError  
   Cause: request_json['userid'] = str(uuid.uuid())  
   ErrorHappenedAt: During Lambda Test Event Invoke  
   ErrorPhase: After/Runtime -- caught by except  
   Fix: request_json['userid'] = str(uuid.uuid1())

8. Error: module cannot access local variable 'ddb_response' where it is not associated with a value  
   ErrorType: UnboundLocalError  
   Cause:  ddb_response == ddbTable.scan(Select='ALL_ATTRIBUTES')  
   ErrorHappenedAt: During Lambda Test Event Invoke  
   ErrorPhase: After/Runtime -- caught by except  
   Fix:  ddb_response = ddbTable.scan(Select='ALL_ATTRIBUTES')  
   ```python Note: == -> Comparison = -> assignment```

9. Error: "Parameter validation failed: Missing required parameter in input: Item"  
   ErrorType: ParamValidationError  
   Cause:  Items=request_json  
   ErrorHappenedAt: During Lambda Test Event Invoke  
   ErrorPhase: After/Runtime -- caught by except  
   Fix: Item=request_json

### Section 02 Sub-Section 01 : Test Locally : October 14, 2026 - October 19, 2026

### What I Learned
- Learned Test events run by using sam local invoke commands, the test event runs on local system
- Need docker engine to run sam local invoke command 
- Created a small file called env.json to give value for Lambda environment variable for local run only

### Commands

1. **sam local invoke -e events/event-post-user.json -n env.json** : SAM invokes lambda function locally in a container with event file as JSON as the input and an environment variable file that overrides the ones in the template. [note: -n does not mean name; it is short for --env-vars. -e is short for --event]

### Errors

1. Error: Running AWS SAM projects locally requires a container runtime    
   ErrorType: container runtime not available   
   Cause: Docker not installed in local system    
   ErrorHappenedAt: During sam local invoke   
   Fix: Installed and start Docker Desktop in local system  

2. Error: Required parameter name not set  
   ErrorType: ValueError   
   Cause: "USERS_TABLE": "ws-serverless-patterns-users-Users"    
   ErrorHappenedAt: During sam local invoke  
   Fix: "USER_TABLES": "ws-serverless-patterns-users-Users"  

3. Error: Required parameter name not set   
   ErrorType: ValueError  
   Cause: container is running in old copy of code, from cache     
   ErrorHappenedAt: During sam local invoke  
   Fix: Rebuild sam build  

4. Error: Expecting property name enclosed in double quotes    
   ErrorType: ParamValidation  
   Cause: the shell stripped the double quotes from the JSON before the CLI received it   
   ErrorHappenedAt:   
   Fix: file://key.json  
   Command: aws dynamodb get-item --table-name ws-serverless-patterns-user-Users --key file://key.json

### Section 03: Connect an API : October 19, 2026

### What I Learned
- Connected the public URLs to the service functions  
- REST API in API Gateway is the collection of resources and methods that are integrated with backend endpoints, Lambda functions or other AWS services
- Implemented events contains HTTP method (GET,POST,DELETE,PUT) in lambda function 
- Added API Service in template along with API endpoint URL
- Founded new error which related to command in terminal

### Error

1. Error: None raised. Spotted while reading the template  
   ErrorType: none  
   Cause: `${AWS-AWS::StackName}; ${AWS::AWS::StackName}-API`    
   ErrorHappenedAt: Found error before executing sam build  
   Fix: `${AWS::StackName}; ${AWS::StackName}-API`

2. Error: export : The term 'export' is not recognized as the name of a cmdlet, function, script file, or operable program.  
   ErrorType: ConnamdNotFoundException (PowerShell)  
   Cause: 
   ```powershell
   export API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name serverless-workshop-m02p01s03 --output text --query "Stacks[0].Outputs[?OutputKey=='APIEndpoint'].OutputValue")
   echo "API endpoint: $API_ENDPOINT"
   ```  
   Definition-cause: export & echo commands support in linux/mac terminal not in windows powershell  
   ErrorHappenedAt: running the workshop's export command in windows Powershell, to read the stack's APIEndpoint output  
   Fix: 
   ```powershell
   $env:API_ENDPOINT = aws cloudformation describe-stacks --stack-name serverless-workshop-m02p01s03 --query "Stacks[0].Outputs[?OutputKey=='APIEndpoint'].OutputValue" --output text`  
   `Write-Output "Your API Endpoint is: $env:API_ENDPOINT"
   ```    
   command: To get/list endpoint URLs **sam list endpoints --stack-name** your-stack-name   
   Alternate-Fix: Type entire API endpoint URL and add /users to get result

### Section 03 Sub-Section 01 : Create User Pool : October 24, 2026

### What I Learned
- 

### Commands


### Errors

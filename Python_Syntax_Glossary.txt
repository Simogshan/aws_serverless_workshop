# Python-Syntax-Glossary.md

## f-string
**Syntax:** `f"...{variable}..."`  
**Example (AWS Workspace):** `f"{event['httpMethod']} {event['resource']}"` 
  where `event = {'httpMethod': 'GET', 'resource': '/users'}`  
**Result:** `"GET /users"`  
**Definition:** Builds a string by inserting variable values directly inside `{}`, evaluated at runtime.  
**More examples:**
- `f"Hello {name}"` where `name = "Alex"` → Result: `"Hello Alex"`
- `f"Total: {price * quantity}"` where `price=10, quantity=3` → Result: `"Total: 30"`

---

## dict-index
**Syntax:** `dictionary[key]`  
**Example (AWS Workspace):** `event['httpMethod']` where `event = {'httpMethod': 'GET', ...}`  
**Result:** `'GET'`  
**Definition:** Square brackets fetch a value by its key name. Raises `KeyError` if the key doesn't exist.  
**More examples:**
- `user['email']` where `user = {'email': 'a@b.com'}` → Result: `'a@b.com'`
- `data['missing_key']` → Result: **raises `KeyError`** (not a value — a crash, worth knowing)

---

## chained-index
**Syntax:** `dictionary[key1][key2]`  
**Example (AWS Workspace):** `event['pathParameters']['userid']` where `event['pathParameters'] = {'userid': 'abc123'}`  
**Result:** `'abc123'`  
**Definition:** Multiple brackets drill into nested dicts, left to right.  
**More examples:**
- `response['body']['data']['id']` → Result: whatever value sits 3 levels deep

---

## dict-literal
**Syntax:** `{key: value}`  
**Example (AWS Workspace):** `{'userid': 'abc123'}` (after chained-index resolves)  
**Result:** `{'userid': 'abc123'}` — a brand new dict object  
**Definition:** Builds a new dictionary inline, at the point of use.  
**More examples:**
- `{'name': 'Alex', 'age': 30}` → Result: `{'name': 'Alex', 'age': 30}`

---

## kwarg (keyword argument)
**Syntax:** `function(param_name=value)`  
**Example (AWS Workspace):** `ddbTable.get_item(Key={'userid': 'abc123'})`  
**Result:** a response dict, e.g. `{'Item': {'userid': 'abc123', 'name': 'Alex'}}` if found, or a dict with NO `'Item'` key at all if not found  
**Definition:** A named argument passed into a function call.  
**More examples:**
- `print("hi", end="")` → Result: prints `hi` with no trailing newline

---

## membership-test
**Syntax:** `value in container`  
**Example (AWS Workspace):** `'Item' in ddb_response`  
**Result:** `True` (if the user was found) or `False` (if not)  
**Definition:** Checks whether a value exists inside a dict's keys or a list's items — always returns a boolean.  
**More examples:**
- `'admin' in ['admin', 'user']` → Result: `True`

---

## getenv-with-default
**Syntax:** `os.getenv('VAR_NAME', fallback_value)`  
**Example (AWS Workspace):** `os.getenv('USERS_TABLE', None)`  
**Result:** `'ws-serverless-patterns-Users'` (the real deployed table name) 
  — or `None` specifically if the env var was never set  
**Definition:** Reads an environment variable; second argument is the fallback used ONLY if that variable isn't set.  
**More examples:**
- `os.getenv('DEBUG', 'false')` when DEBUG isn't set → Result: `'false'`

---

## guarded-conditional-assignment
**Syntax:** `if condition: variable = new_value`  
**Example (AWS Workspace):** `if 'userid' not in request_json: request_json['userid'] = str(uuid.uuid1())`  
**Result:** if `request_json` already had a `'userid'` key → unchanged. 
  If not → `request_json` now has a new `'userid'` key with a generated 
  value like `'a1b2c3d4-...'`
**Definition:** Only assigns/generates a value if a condition is true.  
**More examples:**
- `if 'timestamp' not in data: data['timestamp'] = now()` → adds timestamp only if missing

---

## method-chaining
**Syntax:** `object.method1().method2()`  
**Example (AWS Workspace):** `datetime.now().isoformat()`  
**Result:** `'2026-09-20T14:23:01.123456'` (a string, ISO 8601 format)  
**Definition:** Calls a method, then immediately calls another on THAT result — read strictly left to right.  
**More examples:**
- `"  hello  ".strip().upper()` → Result: `'HELLO'`
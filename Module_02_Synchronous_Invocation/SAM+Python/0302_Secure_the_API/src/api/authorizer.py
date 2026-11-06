
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import re
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

# *** Section 1 : base setup and token validation helper function
is_cold_start = True
keys = {}
user_pool_id = os.getenv('USER_POOL_ID', None)
app_client_id = os.getenv('APPLICATION_CLIENT_ID', None)
admin_group_name = os.getenv('ADMIN_GROUP_NAME', None)


def validate_token(token, region):
    global keys, is_cold_start, user_pool_id, app_client_id
    if is_cold_start:
        # KEYS_URL -- REPLACE WHEN CHANGING IDENTITY PROVIDER!!
        keys_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']
        is_cold_start = False

    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since verification succeeded, you can now safely use the unverified claims
    claims = jwt.get_unverified_claims(token)

    # Additionally you can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    decoded_jwt = jwt.decode(token, key=keys[key_index], audience=app_client_id)
    return decoded_jwt


def lambda_handler(event, context):
    global admin_group_name
    tmp = event['methodArn'].split(':')
    api_gateway_arn_tmp = tmp[5].split('/')
    region = tmp[3]
    aws_account_id = tmp[4]
    # validate the incoming token
    validated_decoded_token = validate_token(event['authorizationToken'], region)
    if not validated_decoded_token:
        raise Exception('Unauthorized')
    principal_id = validated_decoded_token['sub']
    # initialize the policy
    policy = AuthPolicy(principal_id, aws_account_id)
    policy.restApiId = api_gateway_arn_tmp[0]
    policy.region = region
    policy.stage = api_gateway_arn_tmp[1]

    # *** Section 2 : authorization rules
    # Allow all public resources/methods explicitly

    # Add user specific resources/methods
    policy.allow_method(HttpVerb.GET, f"/users/{principal_id}")
    policy.allow_method(HttpVerb.PUT, f"/users/{principal_id}")
    policy.allow_method(HttpVerb.DELETE, f"/users/{principal_id}")
    policy.allow_method(HttpVerb.GET, f"/users/{principal_id}/*")
    policy.allow_method(HttpVerb.PUT, f"/users/{principal_id}/*")
    policy.allow_method(HttpVerb.DELETE, f"/users/{principal_id}/*")

    # Look for admin group in Cognito groups
    # Assumption: admin group always has higher precedence
    if 'cognito:groups' in validated_decoded_token and validated_decoded_token['cognito:groups'][0] == admin_group_name:
        # add administrative privileges
        policy.allow_method(HttpVerb.GET, "users")
        policy.allow_method(HttpVerb.GET, "users/*")
        policy.allow_method(HttpVerb.DELETE, "users")
        policy.allow_method(HttpVerb.DELETE, "users/*")
        policy.allow_method(HttpVerb.POST, "users")
        policy.allow_method(HttpVerb.PUT, "users/*")

    # Finally, build the policy
    auth_response = policy.build()
    return auth_response



# *** Section 3 : authorization policy helper classes
class HttpVerb:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    ALL = "*"

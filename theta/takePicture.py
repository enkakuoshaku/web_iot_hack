# -*- coding: UTF-8 -*-

import json
import requests
from requests.auth import HTTPDigestAuth

url = 'http://192.168.0.179:80/osc/commands/execute'
username = 'THETAYL00142823'
password = '00142823'

headers = {}
headers["Content-Type"]= 'application/json'

payload = {'name':'camera.takePicture'}

r = requests.post(url, auth=HTTPDigestAuth(username,password), headers=headers, data=json.dumps(payload))

print(r)      # 200
print(r.text) # result

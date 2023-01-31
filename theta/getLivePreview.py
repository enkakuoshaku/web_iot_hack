# -*- coding: UTF-8 -*-

import json
import requests
from requests.auth import HTTPDigestAuth

url = 'http://192.168.0.179:80/osc/commands/execute'
username = 'THETAYL00142823'
password = '00142823'

headers = {}
headers["Content-Type"]= 'application/json'

payload = {'name':'camera.getLivePreview'}

response = requests.post(url, auth=HTTPDigestAuth(username,password), headers=headers, data=json.dumps(payload), stream=True)

#HTTP Responseのエラーチェック
try:
    response_status = response.raise_for_status()
except Exception as exc:
    print("Error:{}".format(exc))


# HTTP Responseが正常な場合は下記実行
if response_status == None:
    #各チャンクをwrite()関数でローカルファイルに書き込む
    for chunk in response.iter_content(100000):
        print('chunk:', str(len(chunk)))

    print("ダウンロード・ファイル保存完了")


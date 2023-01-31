from flask import render_template, Flask, Response
import json
import requests
from requests.auth import HTTPDigestAuth
import time

THETAURL = '192.168.0.179:80'

app = Flask(__name__)

def gen_frames1():
    with open('./1.jpg', mode='rb') as f:
        img = f.read()
    cl = 'Content-Length: ' + str(len(img)) + '\r\n'
    while True:
        time.sleep(1/60)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n' + cl.encode() +  b'\r\n' + img + b'\r\n\r\n'

def get_content_length(data):
    i = 0
    for c in data:
        if c > 127:
            break
        i += 1
    s = data[:i].decode()
    p = s.find("Content-Length: ")
    ret = int(s[p+16:])
    print("Content-Length: ", ret)
    return ret, i

def gen_frames():
    url = 'http://' + THETAURL + '/osc/commands/execute'
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
        img = b''
        clen = 0
        for chunk in response.iter_content(100000):
            #time.sleep(0.1)
            print('chunk:', len(chunk), 'imglen:', len(img), 'clen:', clen)
            if not len(img):
                clen, i = get_content_length(chunk)
                img = chunk[i:]
            else:
                img += chunk
                if len(img) >= clen + 200:
                    with open('./out.jpg', mode='wb') as f:
                        f.write(img[:clen])
                    cl = 'Content-Length: ' + str(clen) + '\r\n'
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n' + cl.encode() +  b'\r\n' + img + b'\r\n\r\n'
                    _clen, i = get_content_length(img[clen:])
                    img = img[clen + i:]
                    clen = _clen


@app.route('/video_feed')
def video_feed():
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
@app.route('/index')
def index():   
   user = {'username': 'FZ50'}
   return render_template('index.html')

app.run(port=5000, debug=True)

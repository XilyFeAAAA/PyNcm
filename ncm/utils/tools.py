import re
import base64
import http.cookiejar

import requests

def decode_img(src):
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        return False
    img = base64.urlsafe_b64decode(data)
    with open('./assets/code.png', "wb") as f:
        f.write(img)
    print('请扫描二维码登陆...')

def cookieReader(file_path):
    load_cookiejar = http.cookiejar.LWPCookieJar()
    load_cookiejar.load(file_path, ignore_discard=True, ignore_expires=True)
    load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
    cookies = requests.utils.cookiejar_from_dict(load_cookies)
    return cookies
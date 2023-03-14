import sys
import pathlib
import time
import qrcode
from ncm.utils.tools import decode_img
import http.cookiejar
from ncm.drivers.reqDriver import RequestHandler

class loginBase():
    def __init__(self):
        self._phone: int
        self._email: str
        self._password: str
        self._data: str
        self._ws:RequestHandler

    # 发送登陆请求
    def send(self):
        pass

    def getStatus(self):
        pass

class ppLogin(loginBase):
    # phone and code
    # 需要验证
    def __init__(self, ws):
        super().__init__()
        self._ws = ws

    def send(self, **kwargs):
        route= '/login/cellphone'
        self._phone, self._password = kwargs['phone'], kwargs['password']
        param = {
            'phone': self._phone,
            'password': self._password
        }
        req = self._ws.get(route, params=param)

class epLogin(loginBase):
    #email and password
    # 需要验证
    def __init__(self, ws):
        super().__init__()
        self._ws = ws

    def send(self, **kwargs):
        self._url += '/login'
        self._email, self._password = kwargs['email'], kwargs['password']
        param = {
            'email': self._email,
            'password': self._password
        }
        req = self._ws.get(self._url, param)

class codeLogin(loginBase):
    def __init__(self, ws):
        super().__init__()
        self._ws = ws
        self._generateKey_route = '/login/qr/key?timerstamp={}'
        self._generateCode_route = '/login/qr/create?key={}&qrimg=true&timerstamp={}'
        self._polling_route = '/login/qr/check?key={}&timerstamp={}'


    def send(self):
        res = self._ws.get(self._generateKey_route.format(time.time())).json()
        self._key = res['data']['unikey']
        res2 = self._ws.get(self._generateCode_route.format(self._key, time.time())).json()
        decode_img(res2['data']['qrimg'])
        return self.polling()

    def polling(self):
        self._ws.cookies = http.cookiejar.LWPCookieJar(filename='assets/cookies.txt')
        while True:
            res = self._ws.get(self._polling_route.format(self._key, time.time()))
            if res.json()['code'] == 803:
                self._ws.cookies.save(ignore_expires=True, ignore_discard=True)
                return self._ws.cookies
            elif res.json()['code'] == 800:
                return False
            time.sleep(3)


class anonLogin(loginBase):
    def __init__(self, ws):
        super().__init__()
        self._ws = ws
        self._route = '/register/anonimous'

    def send(self):
        req = self._ws.get(self._route)


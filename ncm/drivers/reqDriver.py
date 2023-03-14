import requests
from requests import cookies
from loguru import logger
from ncm.models.accountModel import requestEnum


class RequestHandler:
    def __init__(self):
        self._ws = requests.session()
        self._baseUrl: str = 'http://localhost:3000'
        self._cookie: cookies.RequestsCookieJar
        self._ws.headers = {'content-type': "application/json",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}

    def set(self, cookie):
        self._cookie = cookie
        self._ws.cookies = self._cookie

    def get(self, route, **kwargs):
        """封装get方法"""
        # 获取请求参数
        params = kwargs.get("params")
        try:
            result = self._ws.get(self._baseUrl + route, params=params)
            return result
        except Exception as e:
            logger.error("Get request error")

    def post(self, route, **kwargs):
        """封装post方法"""
        # 获取请求参数
        params = kwargs.get("params")
        data = kwargs.get("data")
        json = kwargs.get("json")
        try:
            result = requests.post(self._baseUrl + route, params=params, data=data, json=json)
            return result
        except Exception as e:
            logger.error("Post request error")

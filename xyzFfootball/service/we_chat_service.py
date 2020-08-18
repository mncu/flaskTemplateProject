import traceback
import requests
from xyzFfootball.config import config
from xyzFfootball.util.server_exception import ServerException


class WeChatService(object):

    CODE_2_SESSION = 'sns/jscode2session'

    def __init__(self, host, app_id, app_secret):
        self.host = host
        self.app_id = app_id
        self.app_secret = app_secret

    def _request(self, url, data, method="post"):
        url = '{}/{}'.format(self.host, url)
        try:
            if method == "get":
                resp = requests.get(url, params=data, timeout=5)
            else:
                headers = {"Content-Type": "application/json"}
                resp = requests.post(url, json=data, headers=headers, timeout=5)
            data = resp.json()
        except Exception:
            traceback.print_exc()
            raise ServerException(2000)
        if data.get('errcode', 0) == 0:
            return data
        raise ServerException(2000, data['errmsg'])

    def code_2_session(self, code):
        return self._request(self.CODE_2_SESSION, {
            'appid': self.app_id,
            'secret': self.app_secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }, method='get')


FFootball = WeChatService('https://api.weixin.qq.com', config.APP_ID, config.APP_SECRET)

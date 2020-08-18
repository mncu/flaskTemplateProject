

class ServerException(Exception):

    CODE_TO_MSG = {
        -1: 'unknown_error',
        1: 'invalid_token',
        2: 'invalid_user',


        1000: 'activity_does_not_exist',

        2000: 'we_chat_request_error:',

        3000: '数量必须为正整数',
        3001: '找不到该抽签',
        3002: '抽签失败'

    }

    def __init__(self, code, msg=''):
        self.code = code
        self.msg = msg

    def to_json(self):
        return {
            'code': self.code,
            'msg': self.CODE_TO_MSG[self.code] + self.msg
        }


UNKNOWN_ERROR = ServerException(-1)

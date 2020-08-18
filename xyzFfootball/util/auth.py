import traceback
from flask import request
from functools import wraps
from xyzFfootball.service.user_service import UserService
from xyzFfootball.util.server_exception import ServerException, UNKNOWN_ERROR


def uniform_verification(check_token=True):

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                if check_token:
                    token = request.headers.get('F-TOKEN')
                    user_info = UserService.verify_token(token)
                    request.user_info = user_info
                result = func(*args, **kwargs)
                return {
                    'code': 0,
                    'data': result
                }
            except ServerException as e:
                return e.to_json()
            except Exception:
                traceback.print_exc()
                return UNKNOWN_ERROR.to_json()
        return inner
    return wrapper

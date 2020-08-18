import hmac
import binascii
from hashlib import sha1
from xyzFfootball.util.orm_util import db
from xyzFfootball.util.str_util import random_string_generator
from xyzFfootball.orm.user import User, UserToken
from xyzFfootball.util.server_exception import ServerException


class UserService(object):

    @staticmethod
    def verify_token(token):
        token_obj = db.session.query(UserToken).filter_by(token=token).first()
        if not token_obj:
            raise ServerException(1)
        return {
            'user_id': token_obj.user_id,
            'token': token
        }

    @staticmethod
    def register_user(open_id, username, user_avatar):
        user_obj = db.session.query(User).filter_by(open_id=open_id).first()
        if not user_obj:
            user_obj = User(
                open_id=open_id,
                username=username,
                user_avatar=user_avatar
            )
            db.session.add(user_obj)
            db.session.commit()
        return user_obj

    @staticmethod
    def generate_token(user_id):
        hashed = hmac.new(str(user_id).encode('utf8'),
                          random_string_generator(10).encode('utf8'), sha1)
        token = binascii.b2a_base64(hashed.digest())[:-1]
        token_obj = db.session.query(UserToken).filter(UserToken.user_id == user_id).first()
        if token_obj is None:
            token_obj = UserToken(
                user_id=user_id,
                token=token
            )
        token_obj.token = token
        db.session.add(token_obj)
        db.session.commit()
        return token_obj

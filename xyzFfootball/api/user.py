from flask_restful import Resource
from xyzFfootball.api import xyz_api
from xyzFfootball.service.user_service import UserService
from xyzFfootball.service.we_chat_service import FFootball
from flask_restful.reqparse import RequestParser
from xyzFfootball.util.auth import uniform_verification


@xyz_api.resource('/login')
class User(Resource):

    login_parser = RequestParser()
    login_parser.add_argument('code', required=True)
    login_parser.add_argument('name', required=True)
    login_parser.add_argument('user_avatar', required=True)

    @uniform_verification(False)
    def post(self):
        args = self.login_parser.parse_args()
        if args['code'] == 'mncu2jhhhhusdgfsdfsdflkj87':
            data = {
                'openid': 'mncuTest'
            }
        else:
            data = FFootball.code_2_session(args['code'])
        open_id = data['openid']
        user = UserService.register_user(open_id, args['name'], args['user_avatar'])
        token_obj = UserService.generate_token(user.id)
        return {
            'token': token_obj.token
        }

from flask import request
from flask_restful import Resource
from xyzFfootball.api import xyz_api
from xyzFfootball.service.activity import ActivityService
from flask_restful.reqparse import RequestParser
from xyzFfootball.util.auth import uniform_verification


@xyz_api.resource('/activity')
class Activity(Resource):

    detail_parser = RequestParser()
    detail_parser.add_argument('id', type=int, required=True)

    @uniform_verification(True)
    def get(self):
        args = self.detail_parser.parse_args()
        result = ActivityService.get_activity_detail(args['id'])
        return result

    create_parser = RequestParser()
    create_parser.add_argument('name', required=True)
    create_parser.add_argument('end_time', type=int, required=True)

    @uniform_verification(True)
    def post(self):
        user_info = request.user_info
        args = self.create_parser.parse_args()
        activity_obj = ActivityService.\
            create_activity(user_info['user_id'], args['name'], args['end_time'])
        return {
            'activity_id': activity_obj.id
        }

    update_parser = RequestParser()
    update_parser.add_argument('id', type=int, required=True)
    update_parser.add_argument('name', type=str, required=True)
    update_parser.add_argument('end_time', type=int,  default=None)

    @uniform_verification(True)
    def put(self):
        user_info = request.user_info
        args = self.update_parser.parse_args()
        ActivityService.update_activity(args['id'], user_info['user_id'],
                                        args['name'], args['end_time'])
        return {}


@xyz_api.resource('/activity_list')
class ActivityList(Resource):

    get_parser = RequestParser()
    get_parser.add_argument('page', type=int, default=1)
    get_parser.add_argument('limit', type=int, default=10)

    @uniform_verification(True)
    def get(self):
        user_info = request.user_info
        args = self.get_parser.parse_args()
        activity_list = ActivityService.get_user_activity_list(user_info['user_id'],
                                                               args['page'], args['limit'])
        result = []
        for activity, activity_part in activity_list:
            result.append({
                'id': activity.id,
                'name': activity.name,
                'create_time': activity.create_time,
                'end_time': activity.end_time
            })
        return result


@xyz_api.resource('/activity_participant')
class ActivityParticipant(Resource):

    decide_parser = RequestParser()
    decide_parser.add_argument('id', type=int, required=True)
    decide_parser.add_argument('type', type=int, required=True)

    @uniform_verification(True)
    def post(self):
        user_info = request.user_info
        args = self.decide_parser.parse_args()
        ActivityService.join_activity(args['id'], user_info['user_id'], args['type'])
        return {}

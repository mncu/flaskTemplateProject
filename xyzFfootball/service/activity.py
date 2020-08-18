from sqlalchemy import text
from xyzFfootball.util.orm_util import db, generate_sql_text, update_orm_obj
from xyzFfootball.orm.user import User
from xyzFfootball.orm.activity import Activity
from xyzFfootball.util.server_exception import ServerException
from xyzFfootball.orm.activity_participant import ActivityParticipant


class ActivityService(object):

    @staticmethod
    def get_activity_detail(activity_id):
        obj_list = db.session.query(Activity, ActivityParticipant, User).\
            filter(Activity.id == activity_id).\
            join(ActivityParticipant, Activity.id == ActivityParticipant.activity_id).\
            join(User, ActivityParticipant.user_id == User.id).all()
        data = {
            'part_list': [],
            'activity_info': {}
        }
        if not obj_list:
            return data
        data['activity_info'] = {
            'activity_id': obj_list[0][0].id,
            'activity_name': obj_list[0][0].name,
            'activity_create_time': obj_list[0][0].create_time,
            'activity_end_time': obj_list[0][0].end_time
        }
        for activity, activity_part, user in obj_list:
            data['part_list'].append({
                'user_id': user.id,
                'username': user.username,
                'create_time': activity_part.create_time,
                'type': activity_part.type,
                'type_desc': activity_part.type_desc(),
            })
        return data

    @staticmethod
    def create_activity(user_id, name, end_time):
        user_obj = db.session.query(User).filter_by(id=user_id).first()
        if not user_obj:
            raise ServerException(2)
        activity_obj = Activity(
            create_user_id=user_id,
            name=name,
            end_time=end_time
        )
        db.session.add(activity_obj)
        db.session.flush()
        activity_part_obj = ActivityParticipant(
            user_id=user_id,
            activity_id=activity_obj.id,
            is_creator=True
        )
        db.session.add(activity_part_obj)
        db.session.commit()
        return activity_obj

    @staticmethod
    def get_activity(activity_id, create_user_id=None, raise_exc=True):
        sql_text, sql_params = generate_sql_text({
            'activity_id': activity_id,
            'create_user_id': create_user_id
        })
        activity_obj = db.session.query(Activity).filter(text(sql_text)).params(**sql_params).first()
        if not activity_obj and raise_exc:
            raise ServerException(1000)
        return activity_obj

    @staticmethod
    def update_activity(activity, user_id, name, end_time):
        if type(activity) is int:
            activity = ActivityService.get_activity(activity, user_id)
        update_orm_obj(activity, {
            'name': name,
            'end_time': end_time
        })
        db.session.commit()
        return activity

    @staticmethod
    def get_user_activity_list(user_id, page=1, limit=10):
        activity_list = db.session.query(Activity, ActivityParticipant).\
            filter(ActivityParticipant.user_id == user_id).\
            join(Activity, Activity.id == ActivityParticipant.activity_id).\
            order_by(Activity.create_time.desc()).\
            slice((page-1)*limit, page*limit).all()
        return activity_list

    @staticmethod
    def join_activity(activity_id, user_id, join_type=ActivityParticipant.TYPE.agree):
        activity_obj = ActivityService.get_activity(activity_id)
        activity_part_obj = db.session.query(ActivityParticipant).\
            filter_by(activity_id=activity_id, user_id=user_id).first()
        if not activity_part_obj:
            activity_part_obj = ActivityParticipant(
                activity_id=activity_id,
                user_id=user_id,
            )
        activity_part_obj.type = join_type
        db.session.commit()
        return activity_obj

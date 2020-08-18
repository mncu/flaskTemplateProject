import random
from xyzFfootball.util.orm_util import db
from xyzFfootball.orm.user import User
from xyzFfootball.orm.draw import DrawRecord, Draw, DrawParticipant
from xyzFfootball.util.server_exception import ServerException


class DrawService(object):

    @staticmethod
    def get_draw_list(user_id, page, limit):
        return Draw.query.filter_by(create_user_id=user_id).slice((page-1)*limit, page*limit).all()

    @staticmethod
    def get_draw_detail(draw_id):
        result_list = db.session.\
            query(User.name, User.user_avatar, DrawRecord, Draw, DrawParticipant.create_time).\
            join(DrawRecord, DrawRecord.draw_id == Draw.id).\
            join(DrawRecord, DrawRecord.id == DrawParticipant.draw_record_id).\
            join(User, User.id == DrawParticipant.user_id).\
            filter(Draw.id == draw_id).all()
        if not result_list:
            return {}
        draw_result = {
            'name': result_list[0][3].name,
            'id': draw_id,
            'create_time': result_list[0][3].create_time,
            'draw_distribution': {}
        }

        for username, user_avatar, draw_record, draw, join_time in result_list:
            draw_part_list = draw_result['draw_distribution'].setdefault(draw_record.id, [])
            draw_part_list.append({
                'username': username,
                'user_avatar': user_avatar,
                'draw_record_content': draw_record.content,
                'join_time': join_time,
                'total_count': draw_record.total_count,
                'draw_record_id': draw_record.id,
            })

        return draw_result

    @staticmethod
    def create_draw(user_id, name, draw_record_list):
        draw_obj = Draw(
            create_user_id=user_id,
            name=name
        )
        db.session.add(draw_obj)
        db.session.flush()
        for draw_record in draw_record_list:
            if int(draw_record['total_count']) <= 0:
                raise ServerException(3000)
            db.session.add(DrawRecord(
                draw_id=draw_obj.id,
                content=draw_record['content'],
                total_count=draw_record['total_count']
            ))
        db.session.commit()
        return draw_obj

    @staticmethod
    def draw(user_id, draw_id):
        draw_obj = db.session.query(Draw).filter_by(id=draw_id).first()
        if not draw_obj:
            raise ServerException(3001)
        draw_record_list = db.session.query(DrawRecord.id, DrawRecord.total_count).\
            filter(DrawRecord.draw_id == draw_id).all()
        range_list = []
        current_number = 0
        for draw_record in draw_record_list:
            current_number += draw_record[1]
            range_list.append((draw_record[0], current_number))
        random_int = random.randint(1, current_number)

        target_draw_record_id = None
        for range_tuple in range_list:
            if random_int <= range_tuple[1]:
                target_draw_record_id = range_tuple[0]
                break

        draw_participant = DrawParticipant(
            draw_record_id=target_draw_record_id,
            user_id=user_id
        )
        db.session.add(draw_participant)
        try:
            db.session.commit()
            return draw_participant
        except Exception:
            db.session.rollback()
            raise ServerException(3002)

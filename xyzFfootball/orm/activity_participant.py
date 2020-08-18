from time import time
from xyzFfootball.util.orm_util import db
from xyzFfootball.util.orm_util import EmuObject


class ActivityParticipant(db.Model):

    TYPE = EmuObject((
        ('agree', 1, '参加'),
        ('refuse', 2, '拒绝'))
    )

    __tablename__ = 'activity_participant'

    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, index=True, nullable=False)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    create_time = db.Column(db.Integer, index=True, default=time)
    is_creator = db.Column(db.Boolean, default=False)
    type = db.Column(db.SmallInteger, default=TYPE.agree)

    def type_desc(self):
        self.TYPE.get_desc(self.type)

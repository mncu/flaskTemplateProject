from time import time
from xyzFfootball.util.orm_util import db


class Activity(db.Model):

    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    create_user_id = db.Column(db.Integer, index=True, nullable=False)
    name = db.Column(db.String(80))
    create_time = db.Column(db.Integer, index=True, default=time)
    end_time = db.Column(db.Integer)

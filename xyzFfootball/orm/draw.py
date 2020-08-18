from time import time
from xyzFfootball.util.orm_util import db
from sqlalchemy import UniqueConstraint


class Draw(db.Model):

    __tablename__ = 'draw'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_user_id = db.Column(db.Integer, index=True, nullable=False)
    name = db.Column(db.String(40))
    create_time = db.Column(db.Integer, default=time)


class DrawRecord(db.Model):
    __tablename__ = 'draw_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    draw_id = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.String(40))
    total_count = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, default=time)


class DrawParticipant(db.Model):
    __tablename__ = 'draw_participant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    draw_record_id = db.Column(db.Integer, index=True, nullable=False)
    create_time = db.Column(db.Integer, default=time)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    draw_id = db.Column(db.Integer, index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'draw_id', name='uix_user_draw')
    )

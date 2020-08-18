from time import time
from xyzFfootball.util.orm_util import db


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(40))
    user_avatar = db.Column(db.String(1024))

    def __repr__(self):
        return '<User %r>' % self.open_id


class UserToken(db.Model):

    __tablename__ = 'user_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    token = db.Column(db.String(40), unique=True)
    create_time = db.Column(db.Integer, default=time)

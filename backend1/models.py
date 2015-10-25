import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, index=True, nullable=False)
    avatar_id = db.Column(db.Integer, index=True, nullable=False)
    name = db.Column(db.String(80), index=True)
    email = db.Column(db.String(80), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=True)

    def __init__(self, userfk, username, useremail, userphone):
        self.user_fk = userfk
        self.avatar_id = 0
        self.name = username
        self.email = useremail
        self.phone = userphone

    #def __repr__(self):
    #    return '<id: %d, userfk: %d, username: %s, useremail: %s, userphone: %s>' % (self.id, self.user_fk, self.name, self.email, self.phone)

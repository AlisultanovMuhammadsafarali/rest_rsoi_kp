import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, index=True, nullable=False)
    title = db.Column(db.String(60), index=True, nullable=False)
    text = db.Column(db.String(140), index=True, nullable=False)
    dateAdd = db.Column(db.DateTime, index=True, nullable=False)
    dateDelete = db.Column(db.DateTime, index=True, nullable=True)

    def __init__(self, userid, usertitle, usertext):
        self.user_fk = userid
        self.title = usertitle
        self.text = usertext
        self.dateAdd = datetime.utcnow()
        self.dateDelete = None

    #def __str__(self):
    #    d = self.dateAdd
    #    return '<dateAdd: %s>' % (d.strftime("%d.%m.%y %H:%M"))

import sqlite3, uuid
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, index=True, nullable=False)
    namephoto = db.Column(db.String(80), index=True)
    hashphoto = db.Column(db.String(120), index=True, unique=True)
    dateAdd = db.Column(db.DateTime, index=True, nullable=False)
    dateDelete = db.Column(db.DateTime, index=True, nullable=True)

    def __init__(self, userfk, namephoto=None, hashphoto=uuid.uuid4()):
        self.user_fk = userfk
        self.namephoto = namephoto
        self.hashphoto = hashphoto
        self.dateAdd = datetime.utcnow()
        self.dateDelete = None

    #def __repr__(self):
    #    return '<id: %d, userfk: %d, username: %s, useremail: %s, userphone: %s>' % (self.id, self.user_fk, self.name, self.email, self.phone)

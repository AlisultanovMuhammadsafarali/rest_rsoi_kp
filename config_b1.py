from backend1 import app
import os


app.config.update(dict(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///b1.db',
    SECRET_KEY='12453rdfk3j8fwerj9g3rkgjfgiej39sd3rgfrgjrbmbndskjd93'
))
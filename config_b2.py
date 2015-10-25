from backend2 import app
import os


app.config.update(dict(
    DEBUG=True,
#    SQLALCHEMY_DATABASE_URI='sqlite:///b2.db',
    SQLALCHEMY_DATABASE_URI='sqlite:///b2_03.db',
    SECRET_KEY='12453rdfk3j8fwerj9g3rkgjfgiej39sd3rgfrgjrbmbndskjd93'
))
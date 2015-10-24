from frontend import app
import os

# basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(dict(
    DEBUG=True,
    # SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'db.sqlite'),
    SECRET_KEY='12453rdfk3j8fwerj9g3rkgjfgiej39sd3rgfrgjrbmbndskjd93'
))
from backend1 import app
from flask import request, redirect, url_for, abort

import json
from models import db, Photo
db.init_app(app)


@app.route('/photo/add', methods=['POST'])
def addphoto():
    code = 400
    data = {'error': {'message': 'Bad request'}}
    if request.method == 'POST':
        userid = request.json.get('userid')
        if userid and photo is not None:
            photos = Photo(userid, photo)
            db.session.add(user)
            db.session.commit()
            code = 200
            data = {'message': 'ok'}

    return json.dumps(data), code


@app.route('/photo/<useridlist>', methods=['GET'])
@app.route('/photo/<int:userid>', methods=['GET'])
def me(userid=None):
    code = 400
    data = {'error': {'message': 'Bad request'}}
    if request.method == 'GET':
        # userid = request.json.get('userid')
        if userid is not None:
            me = Photo.query.filter_by(user_fk=userid).all()
        else:
            me = Photo.query.filter_by().all()

        if me is not None:
            u = []
            for user in me:
                u.append({'userid': user.user_fk, 'avatarid': user.avatar_id, 'username': user.name, 'email': user.email, 'phone': user.phone})
            code = 200
            data = u
        else:
            code=204
            data = {'error': {'code': code, 'message': 'No Content'}}

    return json.dumps(data), code
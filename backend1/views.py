from backend1 import app
from flask import request, render_template, redirect, url_for, abort, jsonify

import json
from models import db, Users, Friends
from flask.ext.sqlalchemy import Pagination

db.init_app(app)


PER_PAGE = 2

@app.route('/signup', methods=['POST'])
def signup():
    code = 400
    data = {'error': {'message': 'Bad request'}}
    if request.method == 'POST':
        userid = request.json.get('userid')
        username = request.json.get('username')
        email = request.json.get('email')
        phone = request.json.get('phone')
        if userid and username and email and phone is not None:
            user = Users(userid, username, email, phone)
            db.session.add(user)
            db.session.commit()
            code = 200
            data = {'message': 'ok'}

    return json.dumps(data), code


@app.route('/me', methods=['GET'])
@app.route('/me/<int:userid>', methods=['GET'])
def me(userid=None):
    code = 400
    data = {'error': {'message': 'Bad request'}}
    if request.method == 'GET':
        # userid = request.json.get('userid')
        if userid is not None:
            me = Users.query.filter_by(user_fk=userid).all()
        else:
            me = Users.query.filter_by().all()

        #print "__________ ", me[0]
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


@app.route('/users', methods=['GET'])
def users():
    code = 400
    if request.method == 'GET':
        page = int(request.json.get('page')) #int(request.args['page'])
        #record = db.session.query(Users.user_fk, Users.name).all()
        count = Users.query.count()
        record = Users.query.paginate(page, PER_PAGE, count)

        items = record.items
        # return render_template('users1.html', pagination=record)
        if items is not None:
            code = 200
            result = []
            for r in items:
                result.append({'userid':r.user_fk, 'user': r.name})

            result = {'page': record.page,
                      'total': record.total,
                      'pages': record.pages,
                      'items': result}
            return json.dumps(result), code
        else:
            code = 204

    return code


@app.route('/users1/', defaults={'page': 1})
@app.route('/users1/page/<int:page>')
def show_users(page):
    count = Users.query.count()
    users = Users.query.paginate(page, PER_PAGE, error_out=True)
    if not users and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('users1.html',
        pagination=pagination,
        users=users
    )



@app.route('/friend/<int:userid>', methods=['GET'])
@app.route('/friend/<int:userid>/<int:friendid>', methods=['POST'])
def friend(userid=None, friendid=None):
    code = 400
    if request.method == 'GET':
        if userid is not None:
            record = Friends.query.filter_by(user_fk=userid).all()

        if record is not None:
            listid = []
            for r in record:
                listid.append(r.friend_id)

            res = db.session.query(Users).filter(Users.id.in_((listid))).all()

            result = []
            for r in res:
                result.append({'username': r.name, 'email': r.email, 'phone': r.phone})

            code = 200
            data = result
        else:
            code = 204

    if request.method == 'POST':
        if userid and friendid is not None:
            record = Friends(userid, friendid)
            db.session.add(record)
            db.session.commit()
            code = 200

    return json.dumps(data), code
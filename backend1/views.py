from backend1 import app
from flask import request, render_template, redirect, url_for, abort, jsonify

import json
from models import db, Users, Friends
from flask.ext.sqlalchemy import Pagination
from sqlalchemy import literal

db.init_app(app)


PER_PAGE = 2

@app.route('/signup', methods=['POST'])
def signup():
    code = 400
    if request.method == 'POST':
        code = 204
        userid = request.json.get('userid')
        username = request.json.get('username')
        email = request.json.get('email')
        phone = request.json.get('phone')
        if userid and username and email and phone is not None:
            user = Users(userid, username, email, phone)
            db.session.add(user)
            db.session.commit()
            code = 201

    return json.dumps(code)


@app.route('/me', methods=['GET'])
@app.route('/me/<int:userid>', methods=['GET'])
def me(userid=None):
    code = 400
    if request.method == 'GET':
        code=204
        # userid = request.json.get('userid')
        if userid is not None:
            me = Users.query.filter_by(user_fk=userid).all()
        else:
            me = Users.query.filter_by().all()

        #print "__________ ", me[0]
        if me is not None:
            data = []
            for user in me:
                data.append({'userid': user.user_fk, 'avatarid': user.avatar_id, 'username': user.name, 'email': user.email, 'phone': user.phone})
            code = 200
            return json.dumps(data, code)

    return json.dumps(code)


@app.route('/users', methods=['GET'])
def users():
    code = 400
    if request.method == 'GET':
        if 'page' in request.data:
            page = int(request.json.get('page'))
        else:
            return abort(code)

        code = 204
        if page is not None:
            #record = db.session.query(Users.user_fk, Users.name).all()
            count = Users.query.count()
            record = Users.query.paginate(page, PER_PAGE, count)
        else:
            return json.dumps({"message": "No Content"}), code

        if record is not None:
            items = record.items
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
                return json.dumps({"message": "No Content"}), code
        else:
            return json.dumps({"message": "No Content"}), code

    return abort(code)


@app.route('/userlist', methods=['GET'])
def userlist():
    code = 400
    if request.method == 'GET':
        if 'listuserid' in request.data:
            userlist = request.json.get('listuserid')
        else:
            return abort(code)

        if len(userlist) > 0:
            code = 204
            res = db.session.query(Users).filter(Users.user_fk.in_((userlist))).all()

            if res is not None:
                code = 200
                result = []
                for r in res:
                    result.append({'userid': r.user_fk, 'username': r.name, 'email': r.email, 'phone': r.phone})

                return json.dumps(result), code
            else:
                return json.dumps({"message": "No Content"}), code
        else:
            abort(code)

    return abort(code)


@app.route('/friend', methods=['GET'])
@app.route('/friend/<int:userid>/<int:friendid>', methods=['POST'])
def friend(userid=None, friendid=None):
    code = 400
    if request.method == 'GET':
        code = 204
        userid = int(request.json.get('userid'))
        page = int(request.json.get('page'))
        if userid and page is not None:
            count = Friends.query.count()
            record = Friends.query.filter_by(user_fk=userid).paginate(page, PER_PAGE, count)
        else:
            return json.dumps(code)

        if record is not None:
            listid = []
            items = record.items
            for r in items:
                listid.append(r.friend_id)

            result = []
            result = {'page': 1,
                      'total': 0,
                      'pages': 1,
                      'items': result}
            if len(listid) > 0:
                res = db.session.query(Users).filter(Users.user_fk.in_((listid))).all()

                if res is not None:
                    code = 200
                    result = []
                    for r in res:
                        result.append({'username': r.name, 'email': r.email, 'phone': r.phone})
                    result = {'page': record.page,
                              'total': record.total,
                              'pages': record.pages,
                              'items': result}

            return json.dumps(result, code)


    if request.method == 'POST':
        if userid and friendid is not None:
            record = Friends(userid, friendid)
            db.session.add(record)
            db.session.commit()
            code = 201

    return json.dumps(code)


@app.route('/isfriend', methods=['GET'])
def isfriend():
    code = 400
    if request.method == 'GET':
        userid = int(request.json.get('userid'))
        friendid = int(request.json.get('friendid'))
        if userid and friendid is not None:
            q = Friends.query.filter_by(user_fk=userid, friend_id=friendid)
            t = db.session.query(literal(True)).filter(q.exists()).scalar()

            code = 200
            if t is True:
                return json.dumps(True, code)
            else:
                return json.dumps(False, code)
        else:
            code = 204
            return json.dumps(code)

    return json.dumps(code)
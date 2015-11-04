from backend2 import app
from flask import request, redirect, url_for, abort
from sqlalchemy import desc
import json

from models import db, Post, Comments
from flask.ext.sqlalchemy import Pagination

db.init_app(app)

PER_PAGE = 2


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    code = 400
    if request.method == 'GET':
        userid = int(request.json.get('userid'))
        page = int(request.json.get('page'))
        if userid and page is not None:
            count = Post.query.count()
            record = Post.query.filter_by(user_fk=userid).paginate(page, PER_PAGE, count)
        else:
            code = 204
            return code

        if record is not None:
            items = record.items
            if items is not None:
                code = 200
                result = []
                for r in items:
                    d = r.dateAdd
                    result.append({'userid': r.user_fk, 'postid': r.id, 'title': r.title, 'text': r.text, 'dateAdd': str(d.strftime("%d.%m.%y %H:%M"))})

                result = {'page': record.page,
                          'total': record.total,
                          'pages': record.pages,
                          'items': result}
                return json.dumps(result), code
            else:
                code = 204
        else:
            code = 204

    return json.dumps(code)


@app.route('/posts/add', methods=['POST'])
def addposts():
    code = 400
    entry = request.json.get('entry')
    if entry is not None:
        userid = entry['userid']
        title = entry['title']
        text = entry['text']

        query = Post(userid, title, text)
        db.session.add(query)
        db.session.commit()
        code = 201

    return json.dumps({'status_code': code})


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    code = 400
    if request.method == 'GET':
        listpostid = request.json.get('listpostid')
        code=204
        if listpostid is not None:
            allcomments = db.session.query(Comments).filter(Comments.post_id.in_((listpostid))).all()
            # allcomments = Comments.query.filter_by(postid=postid).all()

            if allcomments is not None:
                data = []
                for c in allcomments:
                    d = c.dateAdd
                    data.append({'user_id_whoAdd': c.user_id_whoAdd, 
                                 'postid': c.post_id, 
                                 'text': c.text, 
                                 'dateAdd': str(d.strftime("%d.%m.%y %H:%M")) })

                code = 200
                return json.dumps(data), code

    return json.dumps({'status_code': code})


@app.route('/comments/add', methods=['POST'])
def addcomment():
    code = 400
    comment = request.json.get('comment')
    if comment is not None:
        user_id_whoAdd = comment['userid']
        postid = comment['postid']
        text = comment['text']

        query = Comments(user_id_whoAdd, postid, text)
        db.session.add(query)
        db.session.commit()
        code = 201
    else:
        code = 204

    return json.dumps(code)
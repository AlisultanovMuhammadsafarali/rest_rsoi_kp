from backend2 import app
from flask import request, redirect, url_for, abort
from sqlalchemy import desc
import json

from models import db, Post
db.init_app(app)


@app.route('/entries', methods=['GET'])
@app.route('/entries/<int:userid>', methods=['GET', 'POST'])
def entries(userid=None):
    # userid = request.json.get('userid')
    if userid is not None:
        entry = Post.query.filter_by(user_fk=userid).all() #order_by(desc(Entries.entry_id))
        # entry = db.session.query(Entries).order_by(Entries.entry_id.desc())
    else:
        entry = Post.query.filter_by().all()

    if entry is not None:
        u = []
        for e in entry:
            print str(e.user_fk)+", "+e.title+", "+e.text+", "+str(e.dateAdd)+", "+str(e.dateDelete)
            d = e.dateAdd
            u.append({'userid': e.user_fk, 'title': e.title, 'text': e.text, 'dateAdd': str(d.strftime("%d.%m.%y %H:%M"))})

        code = 200
        data = u
    else:
        code=204
        data = {'error': {'code': code, 'message': 'No Content'}}

    return json.dumps(data), code


@app.route('/entries/add', methods=['POST'])
def addentries():
    code = 400
    data = {'error': {'message': 'Bad request', 'information': 'Incorrect credentials'}}
    entry = request.json.get('entry')
    if entry is not None:
        userid = entry['userid']
        title = entry['title']
        text = entry['text']
        print "userid ", userid
        print "title ", title
        print "text ", text
        query = Post(userid, title, text)
        db.session.add(query)
        db.session.commit()
        code = 200
        data = {'message': "ok"}

    return json.dumps(data), code
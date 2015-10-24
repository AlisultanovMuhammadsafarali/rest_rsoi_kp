from frontend import app
from flask import request, session, g, redirect, url_for, abort, \
                  render_template, flash, make_response, jsonify
import json, requests

headers={'Content-Type': 'application/json'}


@app.route('/')
@app.route('/index')
def index():
    key = request.cookies.get('key')
    response = redirect('/login')
    if key is not None:
        body = json.dumps({'key': key})
        res = requests.post('http://localhost:8003/status', data=body, headers=headers)
        if res.status_code == 200:
            response = redirect('/entries')

    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = json.dumps({'username': request.form['username'], 'password': request.form['password']})
        res = requests.get('http://localhost:8003/login', data=body, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            response = redirect('/entries')
            response.set_cookie('key', value=data['key'])

            return response

    return render_template('login.html', access=False)


@app.route('/logout')
def logout():
    response = make_response(render_template('login.html', access=False))
    response.delete_cookie('key')
    return response


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        username = request.form.get('username')
        email = request.form.get('email')
        phone= request.form.get('phone')

        data1 = {
            'login': login,
            'password': password
        }

        body = json.dumps(data1)
        res_s1 = requests.post('http://localhost:8003/createuser', data=body, headers=headers)

        if res_s1.status_code == 200:
            userid = json.loads(res_s1.text)['userid']

            data2 = {
                'userid': userid,
                'username': username,
                'email': email,
                'phone': phone
            }

            body = json.dumps(data2)
            res_b1 = requests.post('http://localhost:8001/signup', data=body, headers=headers)
            if res_b1.status_code == 200:
                return redirect('/login')
            else:
                flash(json.loads(res_b1)['error'])
                requests.delete('http://localhost:8003/delete', data=body, headers=headers)
        else:
            flash('Try again')

    return render_template('signup.html')


@app.route('/entries', methods=['POST', 'GET'])
def entries():
    if request.method == 'GET':
        key = request.cookies.get('key')
        if key is not None:
            body = json.dumps({'key': key})
            res = requests.post('http://localhost:8003/status', data=body, headers=headers)
            if res.status_code == 200:
                data = json.loads(res.text)
                body = json.dumps(data)
                res_b2 = requests.get('http://localhost:8002/entries/'+str(data['userid']), data=body, headers=headers)

                data = json.loads(res_b2.text)
                return render_template('entries.html', access=True, entries=data)
            else:
                flash(json.loads(res.text)['error'])
        else:
            return redirect('/logout')

    return render_template('entries.html', access=True)


@app.route('/entries/add', methods=['POST'])
def addentries():
    if request.method == 'POST':
        key = request.cookies.get('key')
        if key is not None:
            body = json.dumps({'key': key})
            res = requests.post('http://localhost:8003/status', data=body, headers=headers)
            if res.status_code == 200:
                title = request.form['title']
                text = request.form['text']
                data = {'entry': {'userid': json.loads(res.text)['userid'], 'title': title, 'text': text}}
                body = json.dumps(data)
                res_b2 = requests.post('http://localhost:8002/entries/add', data=body, headers=headers)
                if res_b2.status_code == 200:
                    flash('New entry was successfully posted')
                else:
                    flash('failed add new entry')

                return redirect('/entries')
            else:
                flash(json.loads(res.text)['error'])
                return redirect('/entries')
        else:
            return redirect('/logout')

    return render_template('entries.html')


@app.route('/entries/allusers')
def all():
    key = request.cookies.get('key')
    if key is not None:
        body = json.dumps({'key': key})
        res = requests.post('http://localhost:8003/status', data=body, headers=headers)
        if res.status_code == 200:
            userid = json.loads(res.text)
            body = json.dumps(userid)
            res_b1 = requests.get('http://localhost:8001/me', data=body, headers=headers)
            if res_b1.status_code == 200:
                datame = json.loads(res_b1.text)

            res_b2 = requests.get('http://localhost:8002/entries', headers=headers)
            if res_b2.status_code == 200:
                dataentry = json.loads(res_b2.text)

            r = []
            for usr in datame:
                entr = []
                for e in dataentry:
                    if usr['userid'] == e['userid']:
                        entr.append({'title': e['title'], 'text': e['text']})

                r.append({'username': usr['username'], 'entry': entr})

            return render_template('index.html', entries=r, access=True)
    else:
        return redirect('/logout')

    return redirect('/entries')

from frontend import app
from flask import request, redirect, \
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
            response = redirect('/posts')

    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = json.dumps({'username': request.form['username'], 'password': request.form['password']})
        res = requests.get('http://localhost:8003/login', data=body, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            response = redirect('/posts')
            response.set_cookie('key', value=data['key'])

            return response

    return render_template('login.html', access=False)


@app.route('/logout')
def logout():
    response = make_response(render_template('login.html', access=False))
    response.delete_cookie('key')
    return response


def check():
    key = request.cookies.get('key')
    if key is not None:
        body = json.dumps({'key': key})
        res = requests.post('http://localhost:8003/status', data=body, headers=headers)
        return res
    else:
        return redirect('/logout')


@app.route('/friends', methods=['POST', 'GET'])
@app.route('/friends/<friendid>', methods=['POST', 'GET'])
def friends(friendid=None):
    res = check()
    if res.status_code == 200 and request.method == 'GET':
        res = json.loads(res.text)
        res_b1 = requests.get('http://localhost:8001/me/'+str(res['userid']), headers=headers)
        status = {'user_status_code': True, 'friends_status_code': False}
        if res_b1.status_code != 200:
            status['user_status_code'] = False
            return render_template('layout.html', access=True, status=status)
        user = json.loads(res_b1.text)

        page = 1
        if 'page' in request.args:
            page = request.args.get('page')

        body = json.dumps({'page': page, 'userid': res['userid']})
        friends = requests.get('http://localhost:8001/friend', data=body, headers=headers)
        status['friends_status_code'] = False
        if friends.status_code == 200:
            res = json.loads(friends.text)
            status['friends_status_code'] = True
        return render_template('friends.html', access=True, friend_list=res, user=user, status=status)

    if res.status_code == 200 and request.method == 'POST':
        if 'userid' in request.args:
            res_b1 = requests.post('http://localhost:8001/friend/'+str(res['userid'])+'/'+str(request.args['userid']), headers=headers)
            flash("Ok")
        else:
            return "Not friendid"

    return redirect('/index')


@app.route('/users', methods=['GET', 'POST'])
def users():
    res = check()
    if res.status_code == 200 and request.method == 'GET':
        res = json.loads(res.text)
        res_b1 = requests.get('http://localhost:8001/me/'+str(res['userid']), headers=headers)
        status = {'user_status_code': True, 'users_status_code': False}
        if res_b1.status_code != 200:
            status['user_status_code'] = False
            return render_template('layout.html', access=True, status=False)
        user = json.loads(res_b1.text)

        page = 1
        if 'page' in request.args:
            page = request.args.get('page')

        body = json.dumps({'page': page})
        res_b1 = requests.get('http://localhost:8001/users', data=body, headers=headers)
        status['users_status_code'] = False
        if res_b1.status_code == 200:
            users = json.loads(res_b1.text)
            status['users_status_code'] = True
        return render_template('users.html', access=True, data=body, user=user, user_list=users, status=status)

    return redirect('index')


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



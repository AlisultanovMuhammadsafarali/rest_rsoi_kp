from frontend import app
from flask import request, redirect, \
                  render_template, flash, make_response, jsonify
import json, requests
import viewEntries



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


def check():
    key = request.cookies.get('key')
    if key is not None:
        body = json.dumps({'key': key})
        res = requests.post('http://localhost:8003/status', data=body, headers=headers)
        return res
    else:
        return redirect('/logout')


@app.route('/friend', methods=['GET', 'POST'])
@app.route('/friend/<friendid>', methods=['POST', 'GET'])
def friend(friendid=None):
    res = check()
    if res.status_code == 200:
        res = json.loads(res.text)
        if request.method == 'GET':
            res_b1 = requests.get('http://localhost:8001/friend/'+str(res['userid']), headers=headers)
            data = json.loads(res_b1.text)
            # for d in data:
            #     print "____________ ", d['friendid']

            user = requests.get('http://localhost:8001/me/'+str(res['userid']), headers=headers)
            user = json.loads(user.text)
            return render_template('friends.html', access=True, user=user, friend_list=data)

        if request.method == 'POST':
            if 'userid' in request.args:
                res_b1 = requests.post('http://localhost:8001/friend/'+str(res['userid'])+'/'+str(request.args['userid']), headers=headers)
                flash("Ok")
            else:
                return "Not friendid"

    else:
        flash("error")

    return redirect('/users')



@app.route('/users', methods=['GET'])
# @app.route('/users/<int:page>', methods=['GET'])
def users():
    # if page is None:
    #     page = 1
    #     return 'page = ', page
    # else:
    #     return 'faile'

    res = check()
    if res.status_code == 200 and request.method == 'GET':
        res = json.loads(res.text)
        user = requests.get('http://localhost:8001/me/'+str(res['userid']), headers=headers)
        user = json.loads(user.text)

        page = 1
        if 'page' in request.args:
            page = request.args.get('page')

        body = json.dumps({'page': page})
        res_b1 = requests.get('http://localhost:8001/users', data=body, headers=headers)
        users = json.loads(res_b1.text)

        # print 'page='+str(users['page'])+', total='+str(users['total'])
        # for r in users['items']:
        #     print r


        return render_template('users.html', access=True, data=body, user=user, user_list=users) #jsonify({"users": users})

    return "error"


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



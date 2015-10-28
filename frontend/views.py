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


@app.route('/friend', methods=['POST', 'GET'])
def friend():
    res = check()
    if res.status_code == 200:
        data = json.loads(res.text)

        if request.method == 'GET':
            res_b1 = requests.get('http://localhost:8001/friend/'+str(data['userid']), headers=headers)
            data = json.loads(res_b1.text)
            print "________ ", data
            return data#render_template('friend.html', access=True, friends=data)

        # if request.method == 'POST':
        #    res_b1 = request.post('http://localhost:8001/friend/'+str(data['userid'])+'/'+str(data['friendid']), headers=headers)
        #    data = json.login(res_b1.text)
        #    return data[0]

    else:
        flash("error")



@app.route('/users', methods=['GET'])
def users():
    res = check()
    if res.status_code == 200 and request.method == 'GET':
        data = json.loads(res.text)
        user = requests.get('http://localhost:8001/me/'+str(data['userid']), headers=headers)
        user = json.loads(user.text)
        res_b1 = requests.get('http://localhost:8001/users/name', headers=headers)
        users = json.loads(res_b1.text)

        #print "________________ ", users[0]

        return render_template('users.html', access=True, user=user, user_list=users) #jsonify({"users": users})

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



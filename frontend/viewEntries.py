from frontend import app
from flask import request, redirect, \
                  render_template, flash, make_response
import json, requests

headers={'Content-Type': 'application/json'}


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
                res_b1 = requests.get('http://localhost:8001/me/'+str(data['userid']), headers=headers)
                res_b2 = requests.get('http://localhost:8002/entries/'+str(data['userid']), data=body, headers=headers)

                data = json.loads(res_b2.text)
                user = json.loads(res_b1.text)
                #print "_____________ ", user[0]['username']
                return render_template('entries.html', access=True, entries=data, user=user)
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

            res_b1 = requests.get('http://localhost:8001/me/'+str(userid['userid']), headers=headers)
            user = json.loads(res_b1.text)
            return render_template('index.html', entries=r, user=user, access=True)
    else:
        return redirect('/logout')

    return redirect('/entries')

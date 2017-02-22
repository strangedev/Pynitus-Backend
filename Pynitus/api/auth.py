from flask import json
from flask import request

from Pynitus import app
from Pynitus.auth import authtools
from Pynitus.auth import user_cache


@app.route('/auth/register', methods=['POST'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    privilege = request.args.get('password')

    if username is None or password is None:
        return json.dumps({
            'success': False,
            'reason': 'Missing parameters'
        })

    if privilege is None:
        privilege = 0

    if not user_cache.authorize(request.args.get('token'), privilege):

        return json.dumps({
            'success': False,
            'reason': 'Lacking privilege #thugLife'
        })
    
    success = authtools.register(username, password, privilege)
    
    r = {
        'success': success,
    }

    if not success:
        r['reason'] = 1  # Username already taken

    return json.dumps(r)


@app.route('/auth/login', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    success = False
    user_token = ""

    if username is not None and password is not None:
        user_token = authtools.authenticate(username, password)
        success = len(user_token) > 0

    return json.dumps({
        'success': success,
        'token': user_token
    })
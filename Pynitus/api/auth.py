from flask import json
from flask import request

from Pynitus import app
from Pynitus.auth import authtools
from Pynitus.auth.cache import user_cache


@app.route('/auth/register/<int:privilege>/<string:username>/<string:password>', methods=['POST'])
def register(privilege: int, username: str, password: str):
    if not user_cache.authorize(request.args.get('token'), privilege):

        return json.dumps({
            'success': False,
            'reason': 0  # Lacking privilege  #thugLife
        })
    
    success = authtools.register(username, password, privilege)
    
    r = {
        'success': success,
    }

    if not success:
        r['reason'] = 1  # Username already taken

    return json.dumps(r)


@app.route('/auth/login/<string:username>/<string:password>', methods=['POST'])
def login(username: str, password: str):

    user_token = authtools.authenticate(username, password)
    success = len(user_token) > 0

    return json.dumps({
        'success': success,
        'token': user_token
    })
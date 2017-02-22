from flask import json

from Pynitus import app
from Pynitus.api.request_util import Response, expect, expect_optional
from Pynitus.auth import authtools
from Pynitus.auth import user_cache


@app.route('/auth/register', methods=['POST'])
@expect([('username', str), ('password', str), ('privilege', int)])
@expect_optional([('privilege', int)])
def register(username="", password="", privilege=0):

    if not user_cache.authorize(g._user_token, privilege):

        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })
    
    success = authtools.register(username, password, privilege)
    
    r = {'success': success}

    if not success:
        r['reason'] = Response.USER_EXISTS

    return json.dumps(r)


@app.route('/auth/login', methods=['POST'])
@expect([('username', str), ('password', str)])
def login(username="", password=""):

    success = False
    user_token = ""

    user_token = authtools.authenticate(username, password)
    success = len(user_token) > 0

    r = {'success': success}

    if success:
        r['user_token'] = user_token
    else:
        r['reason'] = Response.BAD_CREDENTIALS

    return json.dumps(r)

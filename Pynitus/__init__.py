from flask import Flask
from flask import request

from Pynitus.framework.pubsub import pub
from Pynitus.io.config_loader import init_config
from Pynitus.model.db.database import db_session, init_db
from Pynitus.pluggable import init_plugins

app = Flask(__name__)
init_config()
init_db()
init_plugins()


@app.teardown_appcontext
def shutdown_session(exception=None):
    # TODO: log exception
    db_session.remove()


@app.before_request
def refresh_user_session():
    user_token = request.args.get('token')
    user_token = user_token if user_token is not None else ""
    pub('user_activity', user_token)


import Pynitus.api.tracks
import Pynitus.api.auth
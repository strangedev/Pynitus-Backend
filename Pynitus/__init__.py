from flask import Flask
from flask import request

from Pynitus.auth.user_cache import init_user_cache
from Pynitus.framework import memcache
from Pynitus.framework.pubsub import pub, init_pubsub
from Pynitus.io.config import init_config
from Pynitus.model.db.database import db_session, init_db
from Pynitus.player.contributor_queue import init_contributor_queue
from Pynitus.player.player import init_player
from Pynitus.player.queue import init_queue
from Pynitus.player.voting import init_voting

app = Flask(__name__)

with app.app_context():
    if memcache.get("pynitus.initialized") is None:
        init_config()
        init_pubsub()
        init_db()
        init_user_cache()
        init_player()
        init_queue()
        init_contributor_queue()
        init_voting()
        memcache.set("pynitus.initialized", True)


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
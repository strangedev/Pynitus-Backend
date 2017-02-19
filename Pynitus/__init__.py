import memcache
from flask import Flask
from flask import g
from flask import request

from Pynitus.framework.pubsub import pub, init_pubsub
from Pynitus.io.config_loader import init_config
from Pynitus.model.db.database import db_session, init_db
from Pynitus.player.contributor_queue import init_contributor_queue
from Pynitus.player.queue import init_queue
from Pynitus.player.voting import init_voting
from Pynitus.pluggable import init_plugins


def get_memcache():
    mc = getattr(g, '_memcache_client', None)
    if mc is None:
        mc = g._memcache_client = memcache.Client(['127.0.0.1'], debug=0)
    return mc


app = Flask(__name__)
init_config()
init_pubsub()
init_db()
init_queue()
init_contributor_queue()
init_voting()
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
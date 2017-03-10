from flask import Flask
from flask import g
from flask import request
from flask_cors import CORS, cross_origin

from Pynitus.auth.user_cache import init_user_cache
from Pynitus.framework import memcache
from Pynitus.framework.pubsub import pub, init_pubsub
from Pynitus.io.config import init_config
from Pynitus.io.storage import init_storage
from Pynitus.model.db.database import db_session, init_db
from Pynitus.player.contributor_queue import init_contributor_queue
from Pynitus.player.player import init_player
from Pynitus.player.queue import init_queue
from Pynitus.player.voting import init_voting
from Pynitus.upload import init_upload

app = Flask(__name__)

if app.debug:
    CORS(app)

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
        init_storage()
        init_upload()
        memcache.set("pynitus.initialized", True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    # TODO: log exception
    db_session.remove()


@app.before_request
def refresh_user_session():
    user_token = request.args.get('token')
    user_token = user_token if user_token is not None else request.remote_addr
    g.user_token = user_token
    pub('user_activity', user_token)


import Pynitus.api.tracks
import Pynitus.api.albums
import Pynitus.api.artists
import Pynitus.api.queue
import Pynitus.api.auth
import Pynitus.api.upload
import Pynitus.api.playlists

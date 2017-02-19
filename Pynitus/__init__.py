from flask import Flask
from flask import request

from Pynitus.io.config_loader import init_config
from Pynitus.model.database import db_session, init_db

app = Flask(__name__)
init_config()
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    # TODO: log exception
    db_session.remove()


import Pynitus.api.tracks
import Pynitus.api.auth
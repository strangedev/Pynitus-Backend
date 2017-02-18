from flask import Flask

from Pynitus.model.database import db_session, init_db

app = Flask(__name__)
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    # TODO: log exception
    db_session.remove()


import Pynitus.api.admin
import Pynitus.api.auth
import Pynitus.api.library
import Pynitus.api.queue
import Pynitus.api.upload

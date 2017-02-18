from Pynitus.Pynitus.model.database import db_session, init_db
from flask import Flask

app = Flask(__name__)
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    # TODO: log exception
    db_session.remove()


import Pynitus.Pynitus.api.library

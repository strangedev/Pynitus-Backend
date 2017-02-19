from Pynitus import db_session
from Pynitus.model.database import persistance
from Pynitus.model.models import User


def create(username: str, password_hashed: bytes, password_salt: bytes) -> User:
    with persistance():
        u = User(username=username, password_hash=password_hashed, password_salt=password_salt)
        db_session.add(u)

    return u

def get(username: str) -> User:
    return db_session.query(User).get(username)

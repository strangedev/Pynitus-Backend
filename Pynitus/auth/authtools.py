import argon2
import os

from Pynitus.auth.cache import user_cache
from Pynitus.framework.pubsub import pub
from Pynitus.io.config_loader import config
from Pynitus.model import users
from Pynitus.model.database import persistance


def authenticate(username: str, password: str) -> str:
    user = users.get(username)

    if user is None:
        del password
        return ""

    hash_result = argon2.argon2_hash(password, user.password_salt)
    del password

    if hash_result == user.password_hash:

        user_token = os.urandom(64).hex()
        while user_cache.exists(user_token):
            user_token = os.urandom(64).hex()

        pub('user_authenticated', user_token, username, user.privilege_level, config['user_ttl'])
        return user_token

    return ""


def register(username: str, password: str, privilege_level: int) -> bool:

    if users.get(username) is not None:
        del password
        return False

    password_salt = os.urandom(512)
    password_hashed = argon2.argon2_hash(password, password_salt)
    del password

    user = users.create(username, password_hashed, password_salt)
    with persistance():
        user.privilege_level = privilege_level

    user_token = os.urandom(64).hex()
    while user_cache.exists(user_token):
        user_token = os.urandom(64).hex()

    pub('user_authenticated', user_token, username, user.privilege_level, config['user_ttl'])
    return True

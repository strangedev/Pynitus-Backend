"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel
    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

import argon2

from Pynitus.framework.pubsub import pub
from Pynitus.io import config
from Pynitus.auth import user_cache
from Pynitus.model import users
from Pynitus.model.db.database import persistance


def authenticate(username: str, password: str) -> str:
    """
    This method is used to authenticate a user using their credentials.
    If the authentication process is successful, a user token is generated
    and published to the user_cache. The user token is also returned by this method
    so that it can be passed to the client as a response.
    If the user couldn't be authenticated, an empty string is returned.

    :param username: The user's username
    :param password: The user's password
    :return: The user's token
    """
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

        pub('user_authenticated', user_token, username, user.privilege_level, config.get('user_ttl'))
        return user_token

    return ""


def register(username: str, password: str, privilege_level: int) -> bool:
    """
    Registers a new user.
    Checks, if the user already exists and only registers a new one, if
    the username isn't already taken.

    :param username: The new user's username
    :param password: The new user's password
    :param privilege_level: The new user's privilege level
    :return: Whether the new user was registered or not
    """

    password_salt = os.urandom(512)
    password_hashed = argon2.argon2_hash(password, password_salt)
    del password

    if users.get(username) is not None:
        return False

    user = users.create(username, password_hashed, password_salt)
    with persistance():
        user.privilege_level = privilege_level

    user_token = os.urandom(64).hex()
    while user_cache.exists(user_token):
        user_token = os.urandom(64).hex()

    pub('user_authenticated', user_token, username, user.privilege_level, config.get('user_ttl'))
    return True

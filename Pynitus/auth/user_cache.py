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

import time

from Pynitus.framework import memcache
from Pynitus.framework.pubsub import sub


def init_user_cache():
    """
    Should be called once on server startup.
    Initializes the persistent cache.
    :return: None
    """
    memcache.set("user_cache.active_users", dict({}))
    sub('user_activity', activity)
    sub('user_authenticated', user_authenticated)


def activity(user_token: str) -> None:
    """
    » Subscribed to user_activity
    Refreshes the last_seen attribute of the user with the given user_token.
    Also invalidates the user's session if the ttl has expired.
    :param user_token: The user token of the active user
    :return: None
    """

    active_users = memcache.get("user_cache.active_users")
    record = active_users.get(user_token)

    if record is None:
        return

    if time.time() - record['last_seen'] > record['ttl']:
        del active_users[user_token]
        memcache.set("user_cache.active_users", active_users)
        return

    active_users[user_token]['last_seen'] = time.time()
    memcache.set("user_cache.active_users", active_users)


def user_authenticated(user_token: str, username: str, privilege_level: int, ttl: int) -> None:
    """
    » Subscribed to user_authenticated
    Populates the cache with info about the user.
    :param user_token: The user token of the user who just authenticated themselves
    :param username: The username token of the user who just authenticated themselves
    :param privilege_level: The privilege level of the user who just authenticated themselves
    :param ttl: The ttl of the record
    :return: None
    """
    print(username, "authenticated.")  # TODO: log event

    active_users = memcache.get("user_cache.active_users")
    active_users[user_token] = {
        'last_seen': time.time(),
        'username': username,
        'privilege_level': privilege_level,
        'ttl': ttl
    }

    old_sessions = []

    for token, record in active_users.items():
        if record['username'] == username and token != user_token:
            old_sessions.append(token)

    for token in old_sessions:
        del active_users[token]

    memcache.set("user_cache.active_users", active_users)


def exists(user_token: str) -> bool:
    """
    :param user_token: A user token
    :return: Whether the user token exists in the cache
    """
    return memcache.get("user_cache.active_users").get(user_token) is not None


def whois(user_token: str) -> str:
    """
    :param user_token: A user token
    :return: The username of the user with the given token
    """
    record = memcache.get("user_cache.active_users").get(user_token)

    if record is None:
        return ""

    return record['username']


def authorize(user_token: str, required_privilege: int) -> bool:
    """
    Used to check whether a user is permitted to perform a certain action.
    :param user_token: The user token of the user who wants to perform the action
    :param required_privilege: The required privilege level to perform the action
    :return: Whether the user is permitted to perform the action
    """

    if required_privilege < 1:
        return True

    record = memcache.get("user_cache.active_users").get(user_token)

    if record is None:
        return False

    if time.time() - record['last_seen'] > record['ttl']:
        active_users = memcache.get("user_cache.active_users")
        del active_users[user_token]
        memcache.set("user_cache.active_users", active_users)
        return False

    return record['privilege_level'] >= required_privilege

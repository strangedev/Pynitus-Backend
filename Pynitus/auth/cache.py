import time

from Pynitus import get_memcache
from Pynitus.framework.pubsub import sub


class UserCache(object):

    def __init__(self):

        if get_memcache().get("user_cache.active_users") is None:
            get_memcache().set("user_cache.active_users", dict({}))

    @property
    def __active(self):
        return get_memcache().get("user_cache.active_users")

    @__active.setter
    def __active(self, v):
        get_memcache().set("user_cache.active_users", v)

    def activity(self, user_token: str) -> None:

        active_users = self.__active

        if active_users.get(user_token) is None:
            return

        active_users[user_token]['last_seen'] = time.time()
        self.__active = active_users

    def user_authenticated(self, user_token: str, username: str, privilege_level: int, ttl: int) -> None:
        print(username, "authenticated.")  # TODO: log event

        active_users = self.__active
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

        self.__active = active_users

    def exists(self, user_token: str) -> bool:
        return self.__active.get(user_token) is not None

    def whois(self, user_token: str) -> str:
        record = self.__active[user_token]

        if record is None:
            return ""

        return record['username']

    def authorize(self, user_token: str, required_privilege: int) -> bool:

        if required_privilege < 1:
            return True

        record = self.__active.get(user_token)

        if record is None:
            return False

        if time.time() - record['last_seen'] > record['ttl']:
            active_users = self.__active
            del active_users[user_token]
            self.__active = active_users
            return False

        return record['privilege_level'] >= required_privilege


user_cache = UserCache()

sub('user_activity', user_cache.activity)
sub('user_authenticated', user_cache.user_authenticated)
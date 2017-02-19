import time

from Pynitus.framework.pubsub import sub


class UserCache(object):

    def __init__(self):
        self.__active = dict({})

    def activity(self, user_token: str) -> None:

        record = self.__active.get(user_token)

        if record is None:
            return

        record['last_seen'] = time.time()

    def user_authenticated(self, user_token: str, username: str, privilege_level: int, ttl: int) -> None:
        print(username, "authenticated.")  # TODO: log event
        self.__active[user_token] = {
            'last_seen': time.time(),
            'username': username,
            'privilege_level': privilege_level,
            'ttl': ttl
        }

        old_sessions = []

        for token, record in self.__active.items():
            if record['username'] == username and token != user_token:
                old_sessions.append(token)

        for token in old_sessions:
            del self.__active[token]

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
            del self.__active[user_token]
            return False

        return record['privilege_level'] >= required_privilege


user_cache = UserCache()

sub('user_activity', user_cache.activity)
sub('user_authenticated', user_cache.user_authenticated)
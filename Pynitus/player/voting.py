from Pynitus import get_memcache
from Pynitus.framework.pubsub import pub, sub


def init_voting():
    set_count(0)
    set_users(set({}))
    set_required(0)

def get_count():
    return get_memcache().get("voting.count")


def set_count(n):
    get_memcache().set("voting.count", n)


def get_users():
    return get_memcache().get("voting.users")


def set_users(u):
    get_memcache().set("voting.users", u)


def get_required():
    return get_memcache().get("voting.required")


def set_required(n):
    get_memcache().set("voting.required", n)


def vote(user_token: bytes):

    users = get_users()

    if user_token not in users:
        users.add(user_token)
        set_users(users)

        get_memcache().incr("voting.count")

    if get_count() >= get_required():
        pub("vote_passed")
        set_count(0)
        set_users(set({}))


sub("required_votes", lambda n: set_required(n))
sub("vote", vote)

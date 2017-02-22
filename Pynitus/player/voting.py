from Pynitus.framework import memcache
from Pynitus.framework.pubsub import pub, sub


def init_voting():
    memcache.set("voting.count", 0)
    memcache.set("voting.users", set({}))
    memcache.set("voting.required", 0)

    sub("required_votes", __set_required_votes)
    sub("vote", vote)


def __set_required_votes(n: int) -> None:
    memcache.set("voting.required", n)


def vote(user_token: bytes):

    users = memcache.get("voting.users")

    if user_token not in users:
        users.add(user_token)
        memcache.set("voting.users", users)
        memcache.incr("voting.count")

    if memcache.get("voting.count") >= memcache.get("voting.required"):
        pub("vote_passed")
        memcache.set("voting.count", 0)
        memcache.set("voting.users", set({}))

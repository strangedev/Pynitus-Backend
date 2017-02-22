from Pynitus.framework import memcache
from Pynitus.framework.pubsub import sub, pub


def init_contributor_queue():
    memcache.set("contributor_queue.items", [])

    sub("queue_add", add)
    sub("queue_remove", remove)
    sub("player.play_next", next)


def add(track_id: int, user_token: str) -> None:
    """
    » Subscribed to queue_add
    Adds a contribution to the queue by it's id
    :param user_token: The user token of the user who added this track
    :param track_id: The track's id
    :return: None
    """
    queue = memcache.get("contributor_queue.items")
    queue.append((track_id, user_token))
    memcache.set("contributor_queue.items", queue)

    pub("required_votes", __required_vote_count())


def remove(track_id: int) -> None:
    """
    » Subscribed to queue_remove
    Removes a contribution from the queue by it's id
    :param track_id: The track's id
    :return: None
    """

    queue = memcache.get("contributor_queue.items")
    queue = [t for t in queue if t[0] is not track_id]
    memcache.set("contributor_queue.items", queue)

    pub("required_votes", __required_vote_count())


def next():
    """
    » Subscribed to queue_next
    Keeps up with the track queue by removing the oldest element from the queue
    :return: None
    """

    queue = memcache.get("contributor_queue.items")

    if len(queue) > 0:
        queue.pop(0)

    memcache.set("contributor_queue.items", queue)
    pub("required_votes", __required_vote_count())


def __required_vote_count():
    """
    :return: The amount of unique contributors to the queue
    """
    return len(set([t[1] for t in memcache.get("contributor_queue.items")]))

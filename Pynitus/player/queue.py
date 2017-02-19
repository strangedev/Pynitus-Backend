from typing import List

from Pynitus import get_memcache
from Pynitus.framework.pubsub import sub


def init_queue():
    set_current(-1)
    set_items([])


def get_current():
    return get_memcache().get("queue.current")


def get_items():
    return get_memcache().get("queue.items")


def set_current(item):
    get_memcache().set("queue.current", item)


def set_items(items):
    get_memcache().set("queue.items", items)


def add(track_id: int, user_token: str) -> None:
    """
    » Subscribed to queue_add
    Adds a track to the queue by it's id
    :param user_token: The user token of the user who added this track
    :param track_id: The track's id
    :return: None
    """
    queue = get_items()
    queue.append(track_id)
    set_items(queue)

def remove(track_id: int) -> None:
    """
    » Subscribed to queue_remove
    Removes a track from the queue by it's id
    :param track_id: The track's id
    :return: None
    """

    queue = get_items()

    if track_id in queue:
        queue.remove(track_id)

    set_items(queue)

def next():
    """
    » Subscribed to queue_next
    Changes the current track by removing the oldest entry from the queue.
    :return: None
    """
    queue = get_items()

    if len(queue) > 0:
        set_current(queue.pop(0))
    else:
        set_current(-1)

    set_items(queue)


sub("queue_add", add)
sub("queue_remove", remove)
sub("queue_next", next)

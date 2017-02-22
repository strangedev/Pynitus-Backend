from tinnitus import remote

from Pynitus.model import tracks
from Pynitus.framework.pubsub import sub


def init_queue():

    sub("queue_add", add)
    sub("queue_remove", remove)


def current():
    with remote() as r:
        current = r.current()
    return current if current is not None else -1


def queue():
    with remote() as r:
        queue = r.queue()
    return queue


def add(track_id: int, user_token: str) -> None:
    """
    » Subscribed to queue_add
    Adds a track to the queue by it's id
    :param user_token: The user token of the user who added this track
    :param track_id: The track's id
    :return: None
    """
    track = tracks.get(track_id)
    with remote() as r:
        r.add(track_id, track.mrl, track.status.backend)


def remove(track_id: int) -> None:
    """
    » Subscribed to queue_remove
    Removes a track from the queue by it's id
    :param track_id: The track's id
    :return: None
    """
    with remote() as r:
        r.remove(track_id)

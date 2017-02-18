from typing import List

from Pynitus.Pynitus.framework.pubsub import sub


class Queue(object):

    def __init__(self):
        self.__current = None  # type: int
        self.__queue = []  # type: List[int]

    def add(self, track_id: int, user_token: str) -> None:
        """
        » Subscribed to queue_add
        Adds a track to the queue by it's id
        :param user_token: The user token of the user who added this track
        :param track_id: The track's id
        :return: None
        """
        self.__queue.append(track_id)

    def remove(self, track_id: int) -> None:
        """
        » Subscribed to queue_remove
        Removes a track from the queue by it's id
        :param track_id: The track's id
        :return: None
        """
        if track_id in self.__queue:
            self.__queue.remove(track_id)

    def next(self):
        """
        » Subscribed to queue_next
        Changes the current track by removing the oldest entry from the queue.
        :return: None
        """
        if len(self.__queue) > 0:
            self.__current = self.__queue.pop(0)
        else:
            self.__current = -1

    @property
    def items(self):
        """
        :return: The items in the queue without the current track
        """
        return self.__queue

    @property
    def current(self):
        """
        :return: The current track
        """
        return self.__current


queue = Queue()

sub("queue_add", queue.add)
sub("queue_remove", queue.remove)
sub("queue_next", queue.next)

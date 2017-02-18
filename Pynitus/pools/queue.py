from typing import List


class Queue(object):

    def __init__(self):
        self.__current = None  # type: int
        self.__queue = []  # type: List[int]

    def add(self, track_id: int) -> None:
        """
        Adds a track to the queue by it's id
        :param track_id: The track's id
        :return: None
        """
        self.__queue.append(track_id)

    def remove(self, track_id: int) -> None:
        """
        Removes a track from the queue by it's id
        :param track_id: The track's id
        :return: None
        """
        if track_id in self.__queue:
            self.__queue.remove(track_id)

    def next(self) -> int:
        """
        Changes the current track by removing the oldest entry from the queue.
        :return: Returns the new current track's id, -1 if queue was empty.
        """
        if len(self.__queue) > 0:
            self.__current = self.__queue.pop(0)
        else:
            self.__current = -1

        return self.__current

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
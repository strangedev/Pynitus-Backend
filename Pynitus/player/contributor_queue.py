from typing import List
from typing import Tuple

from Pynitus.framework.pubsub import sub, pub


class ContributorQueue(object):

    def __init__(self):
        self.__current = None  # type: int
        self.__queue = []  # type: List[Tuple[int, str]]

    def add(self, track_id: int, user_token: str) -> None:
        """
        » Subscribed to queue_add
        Adds a contribution to the queue by it's id
        :param user_token: The user token of the user who added this track
        :param track_id: The track's id
        :return: None
        """
        self.__queue.append((track_id, user_token))

        pub("required_votes", self.required_vote_count)

    def remove(self, track_id: int) -> None:
        """
        » Subscribed to queue_remove
        Removes a contribution from the queue by it's id
        :param track_id: The track's id
        :return: None
        """

        self.__queue = [t for t in self.__queue if t[0] is not track_id]

        pub("required_votes", self.required_vote_count)

    def next(self):
        """
        » Subscribed to queue_next
        Keeps up with the track queue by removing the oldest element from the queue
        :return: None
        """
        if len(self.__queue) > 0:
            self.__queue.pop(0)

        pub("required_votes", self.required_vote_count)

    @property
    def required_vote_count(self):
        """
        :return: The amount of unique contributors to the queue
        """
        return len(set([t[1] for t in self.__queue]))


contributor_queue = ContributorQueue()

sub("queue_add", contributor_queue.add)
sub("queue_remove", contributor_queue.remove)
sub("queue_next", contributor_queue.next)

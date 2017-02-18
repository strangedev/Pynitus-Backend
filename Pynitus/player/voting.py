from pubsub import pub


class Voting(object):

    def __init__(self):
        self.__vote_count = 0
        self.__users_voted = set({})
        self.__queue_contributors = 0

    def set_contributors(self, amount: int) -> None:
        self.__queue_contributors = amount

    def vote(self, user_token: bytes=b""):
        if user_token not in self.__users_voted:
            self.__users_voted.add(user_token)
            self.__vote_count += 1

        if self.vote_count >= self.required_vote_count:
            pub.sendMessage("vote_passed")

        self.__vote_count = 0
        self.__users_voted = set({})

    @property
    def vote_count(self) -> int:
        return self.__vote_count

    @property
    def required_vote_count(self) -> int:
        return self.__queue_contributors

voting = Voting()

pub.subscribe(voting.set_contributors, "queue_contributors")
pub.subscribe(voting.vote, "vote")

from Pynitus.framework.pubsub import pub, sub


class Voting(object):

    def __init__(self):
        self.__vote_count = 0
        self.__users_voted = set({})
        self.__votes_required = 0

    def set_votes_required(self, amount: int) -> None:
        self.__votes_required = amount

    def vote(self, user_token: bytes):
        if user_token not in self.__users_voted:
            self.__users_voted.add(user_token)
            self.__vote_count += 1

        if self.vote_count >= self.required_vote_count:
            pub("vote_passed")

        self.__vote_count = 0
        self.__users_voted = set({})

    @property
    def vote_count(self) -> int:
        return self.__vote_count

    @property
    def required_vote_count(self) -> int:
        return self.__votes_required

voting = Voting()

sub("required_votes", voting.set_votes_required)
sub("vote", voting.vote)

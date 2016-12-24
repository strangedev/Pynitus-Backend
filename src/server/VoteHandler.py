import math
from typing import List

from src.config.ConfigLoader import ConfigLoader
from src.server.SessionHandler import SessionHandler


class VoteHandler(object):

    def __init__(
            self,
            config: ConfigLoader,
            session_handler: SessionHandler,
            vote_successful_callback) -> None:
        self.config = config  # type: ConfigLoader
        self.sessionHandler = session_handler  # type: SessionHandler

        self.users_voted = []  # type: List[int]
        self.required_vote_percentage = config.get("voteSuccessfulPercentage")  # type: float
        self.votes = 0  # type: int
        self.vote_successful_callback = vote_successful_callback

    def getActiveUsers(self) -> int:
        return self.sessionHandler.getCount()

    def newVoting(self) -> None:
        self.users_voted = []
        self.votes = 0

    def getRequiredVotes(self) -> int:
        return int(math.ceil(self.required_vote_percentage * self.getActiveUsers()))

    def voteSuccessful(self) -> bool:
        return self.votes >= self.getRequiredVotes()

    def vote(self, ip_address) -> None:

        if not self.sessionHandler.exists(ip_address):
            return

        if ip_address in self.users_voted:
            return

        self.users_voted.append(ip_address)
        self.votes += 1

        if self.voteSuccessful():
            self.newVoting()
            self.vote_successful_callback()

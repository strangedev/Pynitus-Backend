"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
from typing import List

from src.Config.ConfigLoader import ConfigLoader
from src.Server.SessionHandler import SessionHandler


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

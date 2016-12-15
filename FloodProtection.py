import math
import time


class FloodProtection(object):

    def __init__(self, config, sessionHandler):
        self.config = config
        self.sessionHandler = sessionHandler

        self.users = dict({})
        self.usersVoted = []
        self.requiredVotePercentage = config.get("actionsPerMinute")
        self.votes = 0
        self.voteSuccessfullCallback = voteSuccessfullCallback

    def getActiveUsers(self):
        return self.sessionHandler.getCount()

    def newVoting(self):
        self.usersVoted = []
        self.votes = 0

    def getRequiredVotes(self):
        return math.ceil(self.requiredVotePercentage * self.getActiveUsers())

    def voteSuccessfull(self):
        return self.votes >= self.getRequiredVotes()

    def vote(self, ipAddr):

        if not self.sessionHandler.exists(ipAddr):
            return

        if ipAddr not in self.usersVoted:
            self.usersVoted.append(ipAddr)
            self.votes += 1
            if self.voteSuccessfull():
                self.newVoting()
                self.voteSuccessfullCallback()

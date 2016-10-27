import time
import math


class VoteHandler(object):

    def __init__(self, voteSuccessfullCallback):
        self.users = dict({})
        self.usersVoted = []
        self.maxTimeInactive = 8*60
        self.requiredVotePercentage = 0.66
        self.votes = 0
        self.voteSuccessfullCallback = voteSuccessfullCallback
        self.sessionIdLength = 16

    def getNewSessionId(self):
        validChars = string.ascii_uppercase + string.digits

        while True:
            sessionId = ''.join(
                    random.SystemRandom()
                    .choice(validChars) for _ in range(self.sessionIdLength)
                    )
            if sessionId not in self.users:
                return sessionId

    def userActivity(self, sessionId):

        self.kickInactive()

        self.users[sessionId] = time.time()

    def userStillActive(self, sessionId):

        if time.time() - self.users[sessionId] > self.maxTimeInactive:
            return False
        else:
            return True

    def kickInactive(self):

        usersToRemove = []

        for sessionId in self.users:

            if not self.userStillActive(sessionId):

                usersToRemove.append(sessionId)

        for sessionId in usersToRemove:

            del self.users[sessionId]

    def getActiveUsers(self):

        self.kickInactive()

        return len(self.users.keys())

    def newVoting(self):
        self.usersVoted = []
        self.votes = 0

    def getRequiredVotes(self):
        return math.floor(self.requiredVotePercentage * self.getActiveUsers())

    def voteSuccessfull(self):
        return self.votes >= self.getRequiredVotes()

    def vote(self, sessionId):
        if sessionId not in self.usersVoted:
            self.usersVoted.append(sessionId)
            self.votes += 1
            if self.voteSuccessfull():
                self.newVoting()
                self.voteSuccessfullCallback()

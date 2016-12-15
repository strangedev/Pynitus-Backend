import datetime


class ActionRecord(object):

    def __init__(self, ipAddr):
        self.ipAddr = ipAddr
        self.actionCount = 0
        self.lastAction = datetime.datetime.now()


class FloodProtection(object):

    def __init__(self, config, sessionHandler):
        self.config = config
        self.sessionHandler = sessionHandler

        self.userActions = dict({})
        self.maxActions = config.get("actionsPerMinute")

    def actionsLeft(self, ipAddr):
        return self.maxActions - self.userActions[ipAddr].actionCount

    def actionPermitted(self, ipAddr):
        self.__cleanup()
        self.__registerIfNotExists(ipAddr)

        return self.userActions[ipAddr].actionCount < self.maxActions

    def action(self, ipAddr):
        self.__registerIfNotExists(ipAddr)

        self.userActions[ipAddr].actionCount += 1
        self.userActions[ipAddr].lastAction = datetime.datetime.now()

    def __cleanup(self):
        currentTime = datetime.datetime.now()

        for actionRecord in self.userActions.values():
            if (currentTime - actionRecord.lastAction).seconds > 60:
                actionRecord.actionCount = 0

    def __registerIfNotExists(self, ipAddr):
        if ipAddr not in self.userActions.keys():
            self.userActions[ipAddr] = ActionRecord(ipAddr)

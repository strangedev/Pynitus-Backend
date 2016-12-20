import datetime

from src.data.foundation import DictContainer


class Session(DictContainer.DictContainer):
    """docstring for Session"""
    def __init__(self, ipAddr):
        super(Session, self).__init__()
        self.ipAddr = ipAddr


class SessionHandler(DictContainer.DictContainer):
    """docstring for SessionHandler"""
    def __init__(self, config):
        super(SessionHandler, self).__init__()

        self.config = config

    def activity(self, ipAddr):

        self.__cleanup()

        if not self.exists(ipAddr):
            s = Session(ipAddr)
            self.insert(ipAddr, s)

        self.__updateLastSeen(ipAddr)

    def setAttribute(self, ipAddr, attr, val):
        self.get(ipAddr).set(attr, val)

    def __updateLastSeen(self, ipAddr):
        self.setAttribute(ipAddr, "lastSeen", datetime.datetime.now())

    def __cleanup(self):
        for ipAddr, session in self.getAll():
            if self.__timeout(session):
                self.remove(ipAddr)

    def __timeout(self, session):
        currentTime = datetime.datetime.now()

        return (currentTime - session.get("lastSeen")).seconds \
            >= self.config.get("sessionTimeout")

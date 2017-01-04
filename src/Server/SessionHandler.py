from datetime import datetime
from typing import Any

from src.Config.ConfigLoader import ConfigLoader
from src.Data.Foundation.DictContainer import DictContainer


class Session(DictContainer):
    """docstring for Session"""
    def __init__(self, ip_address: int) -> None:
        super(Session, self).__init__()
        self.ip_address = ip_address  # type: int


class SessionHandler(DictContainer):
    """docstring for SessionHandler"""
    def __init__(self, config: ConfigLoader):
        super(SessionHandler, self).__init__()

        self.config = config  # type: ConfigLoader

    def activity(self, ip_address: int) -> None:

        self.__cleanup()

        if not self.exists(ip_address):
            s = Session(ip_address)
            self.insert(ip_address, s)

        self.__updateLastSeen(ip_address)

    def setAttribute(self, ip_address: int, attr: str, val: Any) -> None:
        self.get(ip_address).set(attr, val)

    def __updateLastSeen(self, ip_address: int) -> None:
        self.setAttribute(ip_address, "lastSeen", datetime.now())

    def __cleanup(self) -> None:
        for ip_address, session in self.getAll():
            if self.__timeout(session):
                self.remove(ip_address)

    def __timeout(self, session: Session) -> bool:
        current_time = datetime.now()

        return (current_time - session.get("lastSeen")).seconds \
            >= self.config.get("sessionTimeout")

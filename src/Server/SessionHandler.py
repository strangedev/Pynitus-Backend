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

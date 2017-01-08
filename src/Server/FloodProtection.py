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
from typing import Dict

from src.Config.ConfigLoader import ConfigLoader
from src.Server.SessionHandler import SessionHandler


class ActionRecord(object):

    def __init__(self, ip_address: int) -> None:
        self.ip_address = ip_address  # type: int
        self.action_count = 0  # type: int
        self.last_action = datetime.now()  # type: datetime


class FloodProtection(object):

    def __init__(self, config: ConfigLoader, session_handler: SessionHandler) -> None:
        self.config = config  # type: ConfigLoader
        self.session_handler = session_handler  # type: SessionHandler

        self.user_actions = dict({})  # type: Dict[int, ActionRecord]
        self.max_actions = config.get("actionsPerMinute")  # type: int

    def actionsLeft(self, ip_address: int) -> int:
        self.__registerIfNotExists(ip_address)
        return self.max_actions - self.user_actions[ip_address].action_count

    def actionPermitted(self, ip_address: int) -> bool:
        self.__cleanup()
        self.__registerIfNotExists(ip_address)

        return self.user_actions[ip_address].action_count < self.max_actions

    def action(self, ip_address: int) -> None:
        self.__registerIfNotExists(ip_address)

        self.user_actions[ip_address].action_count += 1
        self.user_actions[ip_address].last_action = datetime.now()

    def __cleanup(self) -> None:
        current_time = datetime.now()

        for action_record in self.user_actions.values():
            if (current_time - action_record.last_action).seconds > 60:  # TODO: put in Config
                action_record.action_count = 0

    def __registerIfNotExists(self, ip_address: int) -> None:
        if ip_address not in self.user_actions.keys():
            self.user_actions[ip_address] = ActionRecord(ip_address)

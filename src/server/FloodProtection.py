from datetime import datetime
from typing import Dict

from src.config.ConfigLoader import ConfigLoader
from src.server.SessionHandler import SessionHandler


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
            if (current_time - action_record.last_action).seconds > 60:  # TODO: put in config
                action_record.action_count = 0

    def __registerIfNotExists(self, ip_address: int) -> None:
        if ip_address not in self.user_actions.keys():
            self.user_actions[ip_address] = ActionRecord(ip_address)

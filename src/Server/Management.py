from src.Config.ConfigLoader import ConfigLoader
from src.Data.PlaybackQueue import PlaybackQueue
from src.Database.Database import Database
from src.Server.FloodProtection import FloodProtection
from src.Server.HtmlBuilder import HtmlBuilder
from src.Server.Router import Router
from src.Server.SessionHandler import SessionHandler
from src.Server.VoteHandler import VoteHandler


class Management(object):

    def __init__(self, working_dir: str):
        self.__config = ConfigLoader(working_dir)

        HtmlBuilder.setJinja2Environment(self.__config.get("html_dir"))
        HtmlBuilder.setManagement(self)

        self.__session_handler = SessionHandler(self.__config)
        self.__flood_protection = FloodProtection(self.__config, self.__session_handler)
        self.__playback_queue = PlaybackQueue()
        self.__vote_handler = VoteHandler(self.__config, self.__session_handler, self.__playback_queue.playNext)
        self.__database = Database(self.__config)

        self.__playback_queue.onFinishedCallback = self.__vote_handler.newVoting
        self.__playback_queue.onStoppedCallback = self.__vote_handler.newVoting

        self.__router = Router(self)

    @property
    def config(self):
        return self.__config

    @property
    def session_handler(self):
        return self.__session_handler

    @property
    def flood_protection(self):
        return self.__flood_protection

    @property
    def playback_queue(self):
        return self.__playback_queue

    @property
    def vote_handler(self):
        return self.__vote_handler

    @property
    def database(self):
        return self.__database
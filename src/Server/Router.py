from typing import Set

import cherrypy

from src.Server import CherryPyConfig
import src.Views
from src.Views import ROUTES


class Router(object):

    def __init__(self, management):
        self.__management = management
        self.__cherrypy_conf = CherryPyConfig.getConfig(self.__management.config)
        cherrypy.config.update(  # TODO: use real config file
            {'Server.socket_port': self.__management.config.get("hostPort"),
             'log.access_file': self.__management.config.get("accessLogfile"),
             'log.error_file': self.__management.config.get("errorLogfile"),
             'Server.socket_host': self.__management.config.get("hostAddress")}
        )

        cherrypy.quickstart(
            self,
            self.__management.config.get("htmlRootPath"),
            self.__cherrypy_conf
        )

    def _cp_dispatch(self, vpath):

        print(vpath)
        print(ROUTES)

        for route in ROUTES:
            if route.matchesVpath(vpath):
                route.swallowParameters(vpath, cherrypy.request.params)
                return route.view(self.__management)

        # No route found, do something.

    @cherrypy.expose
    def index(self):
        return "No routes were found."

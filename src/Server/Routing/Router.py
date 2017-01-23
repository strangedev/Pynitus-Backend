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


import cherrypy

from src.Server import CherryPyConfig
from src.Server import ServerUtils
from src.Server.Routing.Routes import Routes


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
        try:
            self.__management.session_handler.activity(ServerUtils.getClientIp())
        except Exception as e:
            print(e)
        route = Routes.getRoute(vpath, self.__management, cherrypy.request.params)
        return route if route is not None else vpath

    @cherrypy.expose
    def index(self):
        return Routes.getDefaultRoute(self.__management).index()

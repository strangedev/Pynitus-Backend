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

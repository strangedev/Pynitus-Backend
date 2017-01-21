import cherrypy

from src.Server import ServerUtils
from src.Server.ApiRoute import ApiRoute
from src.Server.HtmlBuilder import HtmlBuilder
from src.Views import addRoute


class ArtistsView(object):

    def __init__(self, management):
        self.__management = management

    # TODO: session activity
    @cherrypy.expose
    def index(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "artists.html",
            ServerUtils.getClientIp(),
            artistNames=self.__management.database.getArtists()
        )

addRoute(ApiRoute(["artists"], ArtistsView))

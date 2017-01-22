import cherrypy

from src.Server import ServerUtils
from src.Server.HtmlBuilder import HtmlBuilder


class AdminViews(object):

    def __init__(self, management):
        self.__management = management

    # TODO: session activity
    @cherrypy.expose
    def index(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "unimported.html",
            ServerUtils.getClientIp(),
            tracks=[(track.title, track.album, track.artist)
                    for track in self.__management.database.getUnimported()]
        )
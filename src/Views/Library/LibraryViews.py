import cherrypy

from src.Server import ServerUtils
from src.Server.Components.HtmlBuilder import HtmlBuilder


class LibraryViews(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self):
        return HtmlBuilder.render(
            "library.html",
            ServerUtils.getClientIp()
        )

    @cherrypy.expose
    def artists(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "artists.html",
            ServerUtils.getClientIp(),
            artistNames=self.__management.database.getArtists()
        )

    @cherrypy.expose
    def albums(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "albums.html",
            ServerUtils.getClientIp(),
            albums=sorted(set([(t.album, t.artist) for t in self.__management.database.getTracks()]))  # TODO: add db feature
        )

    @cherrypy.expose
    def tracks(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "tracks.html",
            ServerUtils.getClientIp(),
            tracks=sorted(set([(t.title, t.album, t.artist) for t in self.__management.database.getTracks()]))  # TODO: add db feature

        )

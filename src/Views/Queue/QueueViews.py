import cherrypy

from src.Server import ServerUtils
from src.Server.Components.HtmlBuilder import HtmlBuilder


class QueueViews(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "queue.html",
            ServerUtils.getClientIp(),
            tracks=self.__management.playback_queue.getQueued()
        )

    @cherrypy.expose
    def add(self):  # FIXME
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "queue.html",
            ServerUtils.getClientIp(),
            tracks=self.__management.playback_queue.getQueued()
        )

    @cherrypy.expose
    def remove(self):  # FIXME
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "queue.html",
            ServerUtils.getClientIp(),
            tracks=self.__management.playback_queue.getQueued()
        )

    @cherrypy.expose
    def start(self):  # FIXME
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "queue.html",
            ServerUtils.getClientIp(),
            tracks=self.__management.playback_queue.getQueued()
        )

    @cherrypy.expose
    def stop(self):  # FIXME
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "queue.html",
            ServerUtils.getClientIp(),
            tracks=self.__management.playback_queue.getQueued()
        )
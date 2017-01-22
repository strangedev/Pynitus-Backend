import cherrypy

from src.Server import ServerUtils
from src.Server.Components.HtmlBuilder import HtmlBuilder


class AdminViews(object):

    def __init__(self, management):
        self.__management = management

    # TODO: session activity
    @cherrypy.expose
    def index(self):
        return "Magic here"

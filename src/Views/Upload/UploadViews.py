import cherrypy

from src.Data.Upload.UploadBroker import UploadBroker
from src.Server import ServerUtils
from src.Server.HtmlBuilder import HtmlBuilder


class NewUploadView(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self):
        return HtmlBuilder.render(
            "add.html",  # TODO: rename template
            ServerUtils.getClientIp(),
            upload_handler_descriptions=UploadBroker.getUploadHandlerDescriptions()
        )


class UploadProcessViews(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self, track_type):
        return "New upload of type: " + track_type

    @cherrypy.expose
    def edit(self, track_type, location):
        return "Editing info of track: " + location

    @cherrypy.expose
    def verify(self, track_type, location):
        return "Verifying track: " + location

import cherrypy

from src.Data.Upload.Upload import Upload
from src.Data.Upload.UploadBroker import UploadBroker
from src.Server import ServerUtils
from src.Server.Components.HtmlBuilder import HtmlBuilder
from src.Views.Library.DetailViews import DetailViews


class NewUploadView(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self):
        return HtmlBuilder.render(
            "new_upload.html",
            ServerUtils.getClientIp(),
            upload_handler_descriptions=UploadBroker.getUploadHandlerDescriptions()
        )


class UploadHandlerViews(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self, track_type):
        upload = UploadBroker.getUpload(track_type)
        # TODO: build upload page
        ServerUtils.setForCurrentSession(self.__management, "upload", upload)
        return "New upload of type: " + track_type

    @cherrypy.expose
    def upload(self, track_type, argument: Upload.UploadArgument=None):
        upload = ServerUtils.getForCurrentSession(self.__management, "upload")
        upload.handle(argument)
        ServerUtils.setForCurrentSession(self.__management, "upload", upload)
        return self.edit(track_type, upload.tag_info)

    @cherrypy.expose
    def edit(self, track_type, tag_info):
        return "Editing tag info of track \n" + str(tag_info)

    @cherrypy.expose
    def verify(self, track_type, **tag_info):
        upload = ServerUtils.getForCurrentSession(self.__management, "upload")
        upload.tag_info = tag_info
        if upload.required_metadata_resent:
            UploadBroker.importIntoDatabase(upload)
            return DetailViews.artist(upload.tag_info["artist"])
        else:
            return self.edit(track_type, upload.tag_info)

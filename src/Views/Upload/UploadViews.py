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
        if upload.required_metadata_present:
            UploadBroker.importIntoDatabase(upload)
            return DetailViews.artist(upload.tag_info["artist"])
        else:
            return self.edit(track_type, upload.tag_info)

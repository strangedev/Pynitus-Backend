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
            albums=self.__management.database.getAlbums()
        )

    @cherrypy.expose
    def tracks(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())
        return HtmlBuilder.render(
            "tracks.html",
            ServerUtils.getClientIp(),
            tracks=sorted(set([(t.title, t.album, t.artist) for t in self.__management.database.getTracks()]))

        )

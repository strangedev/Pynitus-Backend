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

from typing import Dict

import cherrypy

from src.Data.Tagging import TagSupport
from src.Data.Track.Track import Track
from src.Server import ServerUtils
from src.Server.Components.HtmlBuilder import HtmlBuilder
from src.Data.Tagging.TagSupport import TagValue


class UnimportedViews(object):

    def __init__(self, management):
        self.__management = management

    @staticmethod
    def tagInfoToTuples(tag_info: Dict[str, TagValue]):
        tuples = []

        for internal_name, value in tag_info.items():

            required = internal_name in TagSupport.REQUIRED_TAGS
            display_name = TagSupport.getDisplayNameByInternalName(internal_name)

            if TagSupport.isListType(internal_name):
                display_name += " (separated by commas)"
                if value is not None and value != []:
                    value = "".join(value)
                else:
                    value = None

            tuples.append((display_name, internal_name, value, required))

        return sorted(tuples)

    @staticmethod
    def paramsToTagInfo(tag_info: Dict[str, str]):

        for key, value in tag_info.items():
            if TagSupport.isListType(key):
                tag_info[key] = [i.lstrip() for i in value.split(",")]

            if value is "None":
                tag_info[key] = None

        return tag_info

    # TODO: session activity
    @cherrypy.expose
    def index(self):
        self.__management.session_handler.activity(ServerUtils.getClientIp())

        tracks = self.__management.database.getUnimported()

        for track in tracks:

            number_required = len(TagSupport.REQUIRED_TAGS)
            number_complete = number_required

            for internal_name in TagSupport.REQUIRED_TAGS:
                value = track.tag_info[internal_name]
                if value is None or value == []:
                    number_complete -= 1

            track.completeness = "{}/{}".format(number_complete, number_required)

        return HtmlBuilder.render(
            "unimported.html",
            ServerUtils.getClientIp(),
            tracks=tracks
        )

    @cherrypy.expose
    def edit(self, location: str="", previous_track: Track=None):
        edited_track = self.__management.database.getByLocation(location)  # TODO: implement

        if edited_track is None:
            return ":("

        if previous_track is not None:
            edited_track = previous_track

        ServerUtils.setForCurrentSession(self.__management, "edited_track", edited_track)

        return HtmlBuilder.render(
            "edit.html",
            ServerUtils.getClientIp(),
            track=edited_track,
            location=edited_track.location,
            tag_info_tuples=UnimportedViews.tagInfoToTuples(edited_track.tag_info)
        )

    @cherrypy.expose
    def verify(self, location="", **tag_info: Dict[str, str]):
        edited_track = ServerUtils.getForCurrentSession(self.__management, "edited_track")
        edited_track.tag_info = UnimportedViews.paramsToTagInfo(tag_info)

        for internal_name in TagSupport.REQUIRED_TAGS:
            value = edited_track.tag_info[internal_name]
            if value is None or value == []:
                return self.edit(location, edited_track)

        ServerUtils.removeForCurrentSession(self.__management, "edited_track")
        self.__management.database.updateTrack(edited_track)
        self.__management.database.importTrack(edited_track)

        return "Success"
        #return DetailViews.track(edited_track.location)

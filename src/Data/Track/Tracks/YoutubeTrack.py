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

import os

from src.Data import Track
from src.Data.Track.PlaybackHandlers import YoutubePlaybackHandler
from src.Data.Track.UploadHandlers import YoutubeUploadHandler


class YoutubeTrack(Track):

    description = "A Youtube URL"
    uploadHandler = YoutubeUploadHandler

    def isTrackOfType(path_to_record):

        if not os.path.isdir(path_to_record):
            return False

        for item in os.listdir(path_to_record):

            item_name, item_extension = os.path.splitext(item)

            if item_extension == ".yturl":
                return True

        return False

    def __init__(self, artist_name, album_title, title):

        super().__init__(artist_name, album_title, title)

        self.playbackHandlerClass = YoutubePlaybackHandler
        self.url = None

    def restoreFromLocalRecord(self, path_to_record):

        super().restoreFromLocalRecord(path_to_record)

        for item in os.listdir(path_to_record):

            item_name, item_extension = os.path.splitext(item)

            if item_extension == ".yturl":

                self.url = open(os.path.join(path_to_record, item)).read()
                break

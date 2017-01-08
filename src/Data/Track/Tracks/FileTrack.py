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

import mimetypes
import os

from src.Data.Track.PlaybackHandlers import FilePlaybackHandler
from src.Data.Track.UploadHandlers import FileUploadHandler
from src.Data import Track


class FileTrack(Track):
    """
    A Track which uses a local file as it's source
    """

    description = "A Local File"
    uploadHandler = FileUploadHandler

    def __init__(self, artistName, albumTitle, title):
        super().__init__(artistName, albumTitle, title)

        self.playbackHandlerClass = FilePlaybackHandler
        self.filepath = None

    def isTrackOfType(pathToRecord):

        if not os.path.isdir(pathToRecord):
            return False

        for item in os.listdir(pathToRecord):

            if item.endswith(".json"):
                continue

            itemName, itemExtension = os.path.splitext(item)

            if itemExtension in mimetypes.types_map:

                if (mimetypes.types_map[itemExtension].startswith("audio")):
                    # We've got a FileTrack.
                    return True

        return False

    def restoreFromLocalRecord(self, pathToRecord):

        super().restoreFromLocalRecord(pathToRecord)

        for item in os.listdir(pathToRecord):

            if item.endswith(".json"):
                continue

            itemName, itemExtension = os.path.splitext(item)

            if itemExtension not in mimetypes.types_map:
                continue

            if (mimetypes.types_map[itemExtension].startswith("audio")):

                self.filepath = os.path.join(pathToRecord, item)

                break

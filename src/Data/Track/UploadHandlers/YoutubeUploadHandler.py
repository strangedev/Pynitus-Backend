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

from src.Data.Track import UploadHandler
from src.Data.Track.Tracks import YoutubeTrack


class YoutubeUploadHandler(UploadHandler):

    def __init__(self, workingDir):
        super().__init__(workingDir)

        self.attributes.update({
            "URL": ["string", "required", "url"]
        })

    def trackFromUploadedAttributes(self, attributes):

        track = YoutubeTrack(
            attributes["Artist"],
            attributes["Album"],
            attributes["Title"]
        )

        del attributes["Artist"]
        del attributes["Album"]
        del attributes["Title"]

        super().autoImportAttributes(track, attributes)
        super().writeTrackRecord(track)

        artistPath = os.path.join(self.workingDir, track.artistName)
        albumPath = os.path.join(artistPath, track.albumTitle)
        recordPath = os.path.join(albumPath, track.title) + ".rec"
        localFilePath = os.path.join(recordPath, "muzak.yturl")

        fileToWrite = open(localFilePath, 'w+')
        fileToWrite.write(track.url)
        fileToWrite.close()

        return track

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

from src.Data import Track
from src.Data.Track import UploadHandler


class FileUploadHandler(UploadHandler):

    def __init__(self, working_dir):
        super().__init__(working_dir)

        self.attributes.update({
            "File": ["file", "required", None]
        })

    def trackFromUploadedAttributes(self, attributes):

        track = Track.FileTrack(
            attributes["Artist"],
            attributes["Album"],
            attributes["Title"]
        )

        file = attributes["File"]
        fileData = None

        # TODO
        # if not file.content_type.startswith("audio"):
        #    return None

        size = 0
        while True:
            dataChunk = file.file.read(8192)
            if not dataChunk:
                break
            size += len(dataChunk)
            if not fileData:
                fileData = dataChunk
            else:
                fileData += dataChunk

        # fileData = file.read()
        fileName = file.filename

        del attributes["Artist"]
        del attributes["Album"]
        del attributes["Title"]
        del attributes["File"]

        super().autoImportAttributes(track, attributes)
        super().writeTrackRecord(track)

        artistPath = os.path.join(self.workingDir, track.artistName)
        albumPath = os.path.join(artistPath, track.albumTitle)
        recordPath = os.path.join(albumPath, track.title) + ".rec"
        localFilePath = os.path.join(recordPath, fileName)

        fileToWrite = open(localFilePath, 'wb+')
        fileToWrite.write(fileData)
        fileToWrite.close()

        print("File length: ", size)
        track.filepath = localFilePath

        return track

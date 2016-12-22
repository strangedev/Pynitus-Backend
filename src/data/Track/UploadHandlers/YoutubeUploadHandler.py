import os

from src.data.Track import UploadHandler
from src.data.Track.Tracks import YoutubeTrack


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

import mimetypes
import os

from data.Track.PlaybackHandlers.FilePlaybackHandler import FilePlaybackHandler
from data.Track.Track import Track
from data.Track.UploadHandlers import FileUploadHandler


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

import os

from data.Track.PlaybackHandlers.YoutubePlaybackHandler import YoutubePlaybackHandler
from data.Track.Track import Track
from data.Track.UploadHandlers.YoutubeUploadHandler import YoutubeUploadHandler


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

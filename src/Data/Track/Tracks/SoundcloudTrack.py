import os

from src.Data.Track.Track import Track
from src.Data.Track.UploadHandlers import SoundcloudUploadHandler
from src.Data.Track.PlaybackHandlers.SoundcloudPlaybackHandler import SoundcloudPlaybackHandler


class SoundcloudTrack(Track):

    description = "A Soundcloud URL"
    uploadHandler = SoundcloudUploadHandler

    def isTrackOfType(path_to_record):

        if not os.path.isdir(path_to_record):
            return False

        for item in os.listdir(path_to_record):

            item_name, item_extension = os.path.splitext(item)

            if item_extension == ".sndcldurl":
                return True

        return False

    def __init__(self, artist_name, album_title, title):

        super().__init__(artist_name, album_title, title)

        self.playbackHandlerClass = SoundcloudPlaybackHandler
        self.url = None

    def restoreFromLocalRecord(self, path_to_record):

        super().restoreFromLocalRecord(path_to_record)

        for item in os.listdir(path_to_record):

            item_name, item_extension = os.path.splitext(item)

            if item_extension == ".sndcldurl":

                self.url = open(os.path.join(path_to_record, item)).read()
                break

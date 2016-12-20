import json
import mimetypes
import os
from typing import NewType

from src.data.Track.PlaybackHandler import PlaybackHandler

mimetypes.init()  # used as part of isTrackOfType

TrackType = NewType('Track', object)


class Track(object):
    """
    Superclass for all playable and manageable Tracks.
    """

    description = "A Track"

    @staticmethod
    def isTrackOfType(path_to_record):
        return False

    @staticmethod
    def __tryImportingAttribute(attribute_name, dictionary, destination):
        try:
            print("Trying to import: ", attribute_name, " from dict: ", dictionary, " to ", destination)
            setattr(destination, attribute_name, dictionary[attribute_name])
        except Exception as e:
            print("Failed to import", attribute_name, " because of ", e)

    def __init__(self, artist_name: str, album_title: str, title: str, features=None, release_date=None, genre=None,
                 label=None):

        self.playback_handler_class = PlaybackHandler
        self.playback_handler_instance = None
        self.delegate = None
        self.stored_attributes = ["features", "releaseDate", "genre", "label"]
        self.title = title
        self.artist_name = artist_name
        self.album_title = album_title
        self.features = features if features else []
        self.release_date = release_date
        self.genre = genre
        self.label = label

    def play(self, delegate: object):
        """
        Instatiates the playbackHandlerClass and starts
        playback.

        Calls the delegates onFinished() method once playback is done.
        Calls the delegates onStopped() method once playback is stopped
        by stop().
        """

        self.playback_handler_instance = self.playback_handler_class()
        self.playback_handler_instance.play(self, delegate)

    def stop(self):
        """
        Stops the playback using the playbackHandlerClass's
        stop() method.
        """

        self.playback_handler_instance.stop()
        del self.playback_handler_instance

    def onFinished(self):
        self.delegate.onFinished()

    def onStopped(self):
        self.delegate.onStopped()

    def restoreFromLocalRecord(self, path_to_record):

        for item in os.listdir(path_to_record):

            if item == "details.json":

                try:
                    attributes_file = open(os.path.join(path_to_record, item))
                    attribute_file_contents = attributes_file.read()
                    attributes = json.loads(attribute_file_contents)
                    print(attributes)
                    for attribute in self.stored_attributes:
                        Track.__tryImportingAttribute(attribute, attributes, self)

                    attributes_file.close()

                except Exception as e:
                    print(e)

    def storeToFilePath(self, path_to_record):

        details_file = open(os.path.join(path_to_record, "details.json"), "w+")
        details_to_write = dict({})

        for attribute in self.stored_attributes:
            details_to_write[attribute] = getattr(self, attribute)

        details_file.write(json.dumps(details_to_write))
        details_file.close()

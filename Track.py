from typing import NewType

import mimetypes
import os
import json

import PlaybackHandler
import UploadHandler

mimetypes.init()  # used as part of isTrackOfType

TrackType = NewType('Track', object)


class Track(object):
    """
    Superclass for all playable and manageable Tracks.
    """

    description = "A Track"

    def __init__(
        self,
        artistName: str,
        albumTitle: str,
        title: str,
        features=None,
        releaseDate=None,
        genre=None,
        label=None
    ):

        self.playbackHandlerClass = PlaybackHandler.PlaybackHandler
        self.playbackHandlerInstance = None
        self.delegate = None
        self.storedAttributes = ["features", "releaseDate", "genre", "label"]
        self.title = title
        self.artistName = artistName
        self.albumTitle = albumTitle
        self.features = features if features else []
        self.releaseDate = releaseDate
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

        self.playbackHandlerInstance = self.playbackHandlerClass()
        self.playbackHandlerInstance.play(self, delegate)

    def stop(self):
        """
        Stops the playback using the playbackHandlerClass's
        stop() method.
        """

        self.playbackHandlerInstance.stop()
        del self.playbackHandlerInstance

    def onFinished(self):
        self.delegate.onFinished()

    def onStopped(self):
        self.delegate.onStopped()

    def isTrackOfType(pathToRecord):
        return False

    def restoreFromLocalRecord(self, pathToRecord):

        for item in os.listdir(pathToRecord):

            if item == "details.json":

                try:
                    attributeFileContents = open(os.path.join(pathToRecord, item)).read()
                    attributes = json.loads(attributeFileContents)
                    print(attributes)
                    for attribute in self.storedAttributes:
                        Track.__tryImportingAttribute(
                            attribute,
                            attributes,
                            self
                            )

                    attributesFile.close()

                except:
                    pass

    def storeToFilePath(self, pathToRecord):

        detailsFile = open(os.path.join(pathToRecord, "details.json"), "w+")
        detailsToWrite = dict({})

        for attribute in self.storedAttributes:
            detailsToWrite[attribute] = getattr(self, attribute)

        detailsFile.write(json.dumps(detailsToWrite))
        detailsFile.close()

    def __tryImportingAttribute(attributeName, dictionary, destination):
        try:
            print("Trying to import: ", attributeName, " from dict: ", dictionary, " to ", destination)
            setattr(destination, attributeName, dictionary[attributeName])
        except Exception as e:
            print("Failed to import", attributeName, " because of ", e)


class FileTrack(Track):
    """
    A Track which uses a local file as it's source
    """

    description = "A Local File"
    uploadHandler = UploadHandler.FileUploadHandler

    def __init__(self, artistName, albumTitle, title):
        super().__init__(artistName, albumTitle, title)

        self.playbackHandlerClass = PlaybackHandler.FilePlaybackHandler
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


class YoutubeTrack(Track):

    description = "A Youtube URL"
    uploadHandler = UploadHandler.YoutubeUploadHandler

    def __init__(self, artistName, albumTitle, title):

        super().__init__(artistName, albumTitle, title)

        self.playbackHandlerClass = PlaybackHandler.YoutubePlaybackHandler
        self.url = None

    def isTrackOfType(pathToRecord):

        if not os.path.isdir(pathToRecord):
            return False

        for item in os.listdir(pathToRecord):

            itemName, itemExtension = os.path.splitext(item)

            if itemExtension == ".yturl":
                return True

        return False

    def restoreFromLocalRecord(self, pathToRecord):

        super().restoreFromLocalRecord(pathToRecord)

        for item in os.listdir(pathToRecord):

            itemName, itemExtension = os.path.splitext(item)

            if itemExtension == ".yturl":

                self.url = open(os.path.join(pathToRecord, item)).read()

                break


class SoundcloudTrack(Track):

    description = "A Soundcloud URL"
    uploadHandler = UploadHandler.SoundcloudUploadHandler

    def __init__(self, artistName, albumTitle, title):

        super().__init__(artistName, albumTitle, title)

        self.playbackHandlerClass = PlaybackHandler.SoundcloudPlaybackHandler
        self.url = None

    def isTrackOfType(pathToRecord):

        if not os.path.isdir(pathToRecord):
            return False

        for item in os.listdir(pathToRecord):

            itemName, itemExtension = os.path.splitext(item)

            if itemExtension == ".sndcldurl":
                return True

        return False

    def restoreFromLocalRecord(self, pathToRecord):

        super().restoreFromLocalRecord(pathToRecord)

        for item in os.listdir(pathToRecord):

            itemName, itemExtension = os.path.splitext(item)

            if itemExtension == ".sndcldurl":

                self.url = open(os.path.join(pathToRecord, item)).read()

                break
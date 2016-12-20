import json
import mimetypes
import os
from typing import NewType

from data.Track import PlaybackHandler, UploadHandler

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

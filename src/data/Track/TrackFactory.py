import inspect
from typing import NewType

from src.data import Track

TrackFactoryType = NewType('TrackFactory', object)


class TrackFactory(object):
    def __init__(self):
        self.availableTrackTypes = dict({})

        # TODO: Bad practice fix this
        # Get all supported Track types and a reference to their
        # class. These tracks can be instantiated later.
        for name, obj in inspect.getmembers(Track):
            if inspect.isclass(obj):
                if (name.endswith("Track") and name != "Track"):
                    self.availableTrackTypes[name] = obj

    def getTrackFromLocalRecord(self, pathToRecord, artist, album, title):
        for trackType in self.availableTrackTypes:

            if self.availableTrackTypes[trackType].isTrackOfType(pathToRecord):
                print("Track at: " + pathToRecord)

                track = self.availableTrackTypes[
                    trackType](artist, album, title)
                track.restoreFromLocalRecord(pathToRecord)

                return track

        return None

import os
import shutil

from data.Track import TrackFactory


class Database(object):
    """
    Database for Pynitus

    As of right now this is just a crude file system version of a database.
    """
    recordContainerExtension = ".rec"

    def __init__(self, dbDirectory):

        self.dbDirectory = dbDirectory
        self.trackFactory = TrackFactory.TrackFactory()

    def getLocalTracks(self):

        tracks = []

        for artistDir in os.listdir(self.dbDirectory):

            artistPath = os.path.join(self.dbDirectory, artistDir)
            if not os.path.isdir(artistPath):
                continue

            for albumDir in os.listdir(artistPath):

                albumPath = os.path.join(artistPath, albumDir)
                if not os.path.isdir(albumPath):
                    continue

                for trackFilename in os.listdir(albumPath):

                    trackPath = os.path.join(albumPath, trackFilename)
                    trackName, trackContainerExtension \
                        = os.path.splitext(trackFilename)

                    maybeTrack = None

                    if trackContainerExtension == \
                            Database.recordContainerExtension:
                        maybeTrack = self.trackFactory\
                                         .getTrackFromLocalRecord(
                                            trackPath,
                                            artistDir,
                                            albumDir,
                                            trackName
                                            )

                    if maybeTrack:
                        tracks.append(maybeTrack)

        return tracks

    def deleteArtist(self, artist):
        artistPath = os.path.join(self.dbDirectory, artist)
        shutil.rmtree(artistPath)

    def deleteAlbum(self, artist, album):
        albumPath = os.path.join(self.dbDirectory, artist, album)
        shutil.rmtree(albumPath)

    def deleteTrack(self, track):
        trackPath = os.path.join(
            self.dbDirectory,
            track.artistName,
            track.albumTitle,
            track.title
            ) + Database.recordContainerExtension
        shutil.rmtree(trackPath)

    def mergeArtists(self, a1, a2):
        realName = a1.title()

    def mergeAlbums(self, a1, a2):
        realName = a1.title()

    def mergeTracks(self, a1, a2):
        realName = a1.title()
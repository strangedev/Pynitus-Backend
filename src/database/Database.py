import os
import shutil
from typing import List, NewType

from src.data.Track import Track
from src.data.Track import TrackFactory

DatabaseType = NewType('Database', object)


class Database(object):
    """
    Database for Pynitus

    As of right now this is just a crude file system version of a database.
    """
    recordContainerExtension = ".rec"

    def __init__(self, db_directory: str) -> object:

        """

        :param db_directory: path to Directory
        """
        self.dbDirectory = db_directory  # type: str
        self.trackFactory = TrackFactory.TrackFactory() # type: TrackFactory.TrackFactoryType

    def getLocalTracks(self) -> List[Track.TrackType]:

        """

        :return: Tracks of Database
        """
        tracks = []

        for artistDir in os.listdir(self.dbDirectory):

            artist_path = os.path.join(self.dbDirectory, artistDir)
            if not os.path.isdir(artist_path):
                continue

            for albumDir in os.listdir(artist_path):

                album_path = os.path.join(artist_path, albumDir)
                if not os.path.isdir(album_path):
                    continue

                for trackFilename in os.listdir(album_path):

                    track_path = os.path.join(album_path, trackFilename)
                    track_name, track_container_extension \
                        = os.path.splitext(trackFilename)

                    maybe_track = None

                    if track_container_extension == \
                            Database.recordContainerExtension:
                        maybe_track = self.trackFactory\
                                         .getTrackFromLocalRecord(
                                            track_path,
                                            artistDir,
                                            albumDir,
                                            track_name
                                            )

                    if maybe_track:
                        tracks.append(maybe_track)

        return tracks

    def deleteArtist(self, artist: str) -> None:
        """

        :param artist: Artist to delete
        """
        artist_path = os.path.join(self.dbDirectory, artist)
        shutil.rmtree(artist_path)

    def deleteAlbum(self,
                    artist: str,
                    album: str
                    ) -> None:
        """

        :param artist: Artist of Album
        :param album: Album to delete
        """
        album_path = os.path.join(self.dbDirectory, artist, album)
        shutil.rmtree(album_path)

    def deleteTrack(self, track: str) -> None:
        """

        :param track: Track to delete
        """
        track_path = os.path.join(
            self.dbDirectory,
            track.artistName,
            track.albumTitle,
            track.title
            ) + Database.recordContainerExtension
        shutil.rmtree(track_path)

    def mergeArtists(self,
                     a1: str,
                     a2: str
                     ) -> None:
        # TODO: Implement
        # realName = a1.title()
        pass

    def mergeAlbums(self,
                    a1: str,
                    a2: str
                    ) -> None:
        # TODO: Implement
        # realName = a1.title()
        pass

    def mergeTracks(self,
                    a1: str,
                    a2: str) -> None:
        # TODO: Implement
        # realName = a1.title()
        pass
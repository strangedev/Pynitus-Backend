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
        self.db_directory = db_directory  # type: str
        self.trackFactory = TrackFactory.TrackFactory()  # type: TrackFactory.TrackFactoryType

    def getLocalTracks(self) -> List[Track.TrackType]:

        """

        :return: Tracks of Database
        """
        tracks = []

        for artist_dir in os.listdir(self.db_directory):

            artist_path = os.path.join(self.db_directory, artist_dir)
            if not os.path.isdir(artist_path):
                continue

            for album_dir in os.listdir(artist_path):

                album_path = os.path.join(artist_path, album_dir)
                if not os.path.isdir(album_path):
                    continue

                for track_filename in os.listdir(album_path):

                    track_path = os.path.join(album_path, track_filename)
                    track_name, track_container_extension \
                        = os.path.splitext(track_filename)

                    maybe_track = None

                    if track_container_extension == \
                            Database.recordContainerExtension:
                        maybe_track = self.trackFactory\
                                         .getTrackFromLocalRecord(
                                            track_path,
                                            artist_dir,
                                            album_dir,
                                            track_name
                                            )

                    if maybe_track:
                        tracks.append(maybe_track)

        return tracks

    def deleteArtist(self, artist: str) -> None:
        """

        :param artist: Artist to delete
        """
        artist_path = os.path.join(self.db_directory, artist)
        shutil.rmtree(artist_path)

    def deleteAlbum(self,
                    artist: str,
                    album: str
                    ) -> None:
        """

        :param artist: Artist of Album
        :param album: Album to delete
        """
        album_path = os.path.join(self.db_directory, artist, album)
        shutil.rmtree(album_path)

    def deleteTrack(self, track: Track.TrackType) -> None:
        """

        :param track: Track to delete
        """
        track_path = os.path.join(
            self.db_directory,
            track.artist_name,
            track.album_title,
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
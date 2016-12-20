from typing import List
from typing import Dict
from typing import NewType

from src.data.Track import Track
from src.database.Database import Database
from src.database.Database import DatabaseType
from src.config.ConfigLoader import ConfigLoader
from src.config.ConfigLoader import ConfigLoaderType

MusicLibraryType = NewType('MusicLibrary', object)


class MusicLibrary(object):
    def __init__(self, config: ConfigLoaderType) -> None:

        """

        :param config: ConfigLoader.ConfigLoaderType
        """
        self.musicDirectory = config.get("musicDirectory")  # type: str
        self.db = Database(self.musicDirectory)  # type: DatabaseType
        self.entries = dict({})  # type: Dict[str, dict]

        self.__generateIndexes()
        #self.__cleanup()

    def __generateIndexes(self) -> None:
        """
        generates an construct entry for tracks given by Database based on local Track Dictionary
        """
        tracks = self.db.getLocalTracks()
        for track in tracks:
            try:
                self.constructEntry(track)
            except Exception as e:
                print(e)

    def __mergeArtists(self, fst_artist_name, snd_artist_name) -> None:
        pass

    def __mergeAlbums(self, fst_album_title, snd_album_title) -> None:
        pass

    def __mergeTracks(self, fst_album_title, snd_album_title) -> None:
        pass

    def __cleanup(self) -> None:
        pass

    def getArtists(self) -> List[str]:
        """

        :return: All Artist in entries of Music Library
        """
        return list(self.entries.keys())

    def getAlbumsForArtist(self, artist: str) -> List[str]:
        """

        :param artist: str: name of Artist
        :return: Names of Albums based on given Artist
        """
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        return list(self.entries[artist].keys())

    def getAlbums(self) -> List[str]:
        """

        :return: All Album stored in MusicLibrary
        """
        return [item for sublist in [self.getAlbumsForArtist(artist)
                for artist in self.getArtists()] for item in sublist]

    def getTracksForAlbumOfArtist(
        self,
        artist: str,
        album: str
    ) -> List[Track.TrackType]:
        """
        :param artist: Artist to Album
        :param album: Album to get Tracks from
        :return: Tracks of Album
        :rtype: List[Track.TrackType]
        """
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        if album not in [album for album in self.getAlbumsForArtist(artist)]:
            raise Exception("Artist has no such album.")

        return list(self.entries[artist][album].values())

    def getTracksForArtist(self, artist: str) -> List[Track.TrackType]:
        """

        :param artist: Artist to get Tracks from
        :return: List of Tracks for given Artist
        """
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        return [item for sublist in
                [self.entries[artist][album].values()
                    for album in self.entries[artist].keys()]
                for item in sublist]

    def getTracks(self) -> List[Track.TrackType]:

        """

        :return: All Tracks stored in Music Library as List
        """
        return [item for sublist in
                [self.getTracksForArtist(artist)
                    for artist in self.getArtists()] for item in sublist]

    def constructEntry(self, track: Track.TrackType) -> None:
        """

        :param track: Track to add in entries of Music Library
        """
        self.__addArtist(track.artistName)
        self.__addAlbum(track.artistName, track.albumTitle)
        self.__addTrack(track.artistName, track.albumTitle, track)

    def __addArtist(self, artist: str) -> None:

        """

        :param artist: Artist to add in entries of Music Library
        """
        if artist not in self.entries:
            self.entries[artist] = dict({})

    def __addAlbum(self, artist: str, album: str) -> None:
        """

        :param artist: Artist to Album
        :param album: Album to add in entries of Music Library
        """
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        self.entries[artist][album] = dict({})

    def __addTrack(
        self,
        artist: str,
        album: str,
        track: Track.TrackType
    ) -> None:
        """

        :rtype: None
        :param artist: str: to find dict of artist
        :param album: str: to find dict of album to artist
        :param track: Track.TrackType: playable and manageable Object
        """
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        if album not in [album for album in self.getAlbumsForArtist(artist)]:
            raise Exception("Album doesn't exist")

        self.entries[artist][album][track.title] = track

    def deleteTrack(self, track: Track.TrackType) -> None:
        """

        :param track: Track to delete
        """
        self.db.deleteTrack(track)
        del self.entries[track.artistName][track.albumTitle][track.title]

    def deleteAlbum(self, artist: str, album: str) -> None:
        """

        :param artist: Artist of Album
        :param album: Album to delete
        """
        self.db.deleteAlbum(artist, album)
        del self.entries[artist][album]

    def deleteArtist(self, artist: str) -> None:
        """

        :param artist: Artist to delete
        """
        self.db.deleteArtist(artist)
        del self.entries[artist]

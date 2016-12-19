from typing import List
from typing import NewType

import Track
import TrackFactory
import Database

MusicLibraryType = NewType('MusicLibrary', object)


class MusicLibrary(object):

    def __init__(self, config):

        self.musicDirectory = config.get("musicDirectory")
        self.db = Database.Database(self.musicDirectory)
        self.entries = dict({})

        self.__generateIndexes()
        self.__cleanup()

    def __generateIndexes(self) -> None:
        tracks = self.db.getLocalTracks()
        for track in tracks:
            try:
                self.addTrack(track)
            except Exception as e:
                print(e)

    def __mergeArtists(self, fstArtistName, sndArtistName) -> None:
        pass

    def __mergeAlbums(self, fstAlbumTitle, sndAlbumTitle) -> None:
        pass

    def __mergeTracks(self, fstAlbumTitle, sndAlbumTitle) -> None:
        pass

    def __cleanup(self) -> None:
        pass

    def getArtists(self) -> List[str]:
        return list(self.entries.keys())

    def getAlbumsForArtist(self, artist: str) -> List[str]:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        return list(self.entries[artist].keys())

    def getAlbums(self) -> List[str]:
        return [item for sublist in [self.getAlbumsForArtist(artist)
                for artist in self.getArtists()] for item in sublist]

    def getTracksForAlbumOfArtist(
        self,
        artist: str,
        album: str
    ) -> List[Track.TrackType]:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        if album not in [album for album in self.getAlbumsForArtist(artist)]:
            raise Exception("Artist has no such album.")

        return list(self.entries[artist][album].values())

    def getTracksForArtist(self, artist: str) -> List[Track.TrackType]:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        return [item for sublist in
                [self.entries[artist][album].values()
                    for album in self.entries[artist].keys()]
                for item in sublist]

    def getTracks(self) -> List[Track.TrackType]:

        return [item for sublist in
                [self.getTracksForArtist(artist)
                    for artist in self.getArtists()] for item in sublist]

    def addTrack(self, track: Track.TrackType) -> None:
        self.__addArtist(track.artistName)
        self.__addAlbum(track.artistName, track.albumTitle)
        self.__addTrack(track.artistName, track.albumTitle, track)

    def __addArtist(self, artist: str) -> None:

        if artist not in self.entries:
            self.entries[artist] = dict({})

    def __addAlbum(self, artist: str, album: str) -> None:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        self.entries[artist][album] = dict({})

    def __addTrack(
        self,
        artist: str,
        album: str,
        track: Track.TrackType
    ) -> None:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        if album not in [album for album in self.getAlbumsForArtist(artist)]:
            raise Exception("Album doesn't exist")

        self.entries[artist][album][track.title] = track

    def deleteTrack(self, track: Track.TrackType) -> None:
        self.db.deleteTrack(track)
        del self.entries[track.artistName][track.albumTitle][track.title]

    def deleteAlbum(self, artist: str, album: str) -> None:
        self.db.deleteAlbum(artist, album)
        del self.entries[album.artistName].albums[album.title]

    def deleteArtist(self, artist: str) -> None:
        self.db.deleteArtist(artist)
        del self.entries[artist]

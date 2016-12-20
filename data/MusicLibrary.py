from typing import List
from typing import NewType

import Database
import UnicodeUtils
from data import Track

MusicLibraryType = NewType('MusicLibrary', object)


class MusicLibrary(object):

    def __init__(self, config):

        self.musicDirectory = config.get("musicDirectory")
        self.db = Database.Database(self.musicDirectory)
        self.entries = dict({})

        self.__generateIndexes()
        #self.__cleanup()

    def __generateIndexes(self) -> None:
        tracks = self.db.getLocalTracks()
        print(tracks)
        for track in tracks:
            try:
                self.addTrack(track)
            except Exception as e:
                print(e)

    def __cleanup(self) -> None:
        # TODO: find a faster way to do this (O(n^2) currently)
        for artist in self.entries:
            for other in self.entries:
                if UnicodeUtils.unicode_compare(artist, other):
                    self.db.mergeArtists(artist, other)

        for artist in self.entries:
            for album in self.entries[artist]:
                for other in self.entries[artist]:
                    if UnicodeUtils.unicode_compare(album, other):
                        self.db.mergeAlbums(album, other)

        for artist in self.entries:
            for album in self.entries[artist]:
                for track in self.entries[artist][album]:
                    for other in self.entries[artist][album]:
                        if UnicodeUtils.unicode_compare(track, other):
                            self.db.mergeTracks(track, other)

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
    ) -> List[object]:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        if album not in [album for album in self.getAlbumsForArtist(artist)]:
            raise Exception("Artist has no such album.")

        return list(self.entries[artist][album].values())

    def getTracksForArtist(self, artist: str) -> List[object]:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        return [item for sublist in
                [self.entries[artist][album].values()
                    for album in self.entries[artist].keys()]
                for item in sublist]

    def getTracks(self) -> List[object]:

        return [item for sublist in
                [self.getTracksForArtist(artist)
                    for artist in self.getArtists()] for item in sublist]

    def addTrack(self, track: object) -> None:
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
        track: object
    ) -> None:
        if artist not in self.entries:
            raise Exception("Artist doesn't exist")

        if album not in [album for album in self.getAlbumsForArtist(artist)]:
            raise Exception("Album doesn't exist")

        self.entries[artist][album][track.title] = track

    def deleteTrack(self, track: object) -> None:
        self.db.deleteTrack(track)
        del self.entries[track.artistName][track.albumTitle][track.title]

    def deleteAlbum(self, artist: str, album: str) -> None:
        self.db.deleteAlbum(artist, album)
        del self.entries[album.artistName].albums[album.title]

    def deleteArtist(self, artist: str) -> None:
        self.db.deleteArtist(artist)
        del self.entries[artist]

from typing import Any, Dict

from src.data.Track.Track import Track


class Database(object):

    def refreshDB(self) -> None:
        return NotImplemented

    def addTrack(
            self,
            title: str,
            artist: str,
            album: str,
            type: str,
            location: str,
            **kwargs
    ) -> None:
        return NotImplemented

    def getTracksByArtist(self, artist: str) -> [Track]:
        return NotImplemented

    def getTracksByAlbum(self,
                         artist: str,
                         album: str) -> [Track]:
        return NotImplemented

    def getTrack(self,
                 title: str,
                 artist: str,
                 album: str) -> Track:
        return NotImplemented

    def getUnavailable(self) -> [Track]:
        return NotImplemented

    def getUnimported(self) -> [Track]:
        return NotImplemented


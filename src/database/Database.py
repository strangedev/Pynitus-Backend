from typing import Any, Dict, List

from src.data.Track.Track import Track
from src.data.Track.TrackFactory import TrackFactory
from src.database.IDatabaseAdapter import IDatabaseAdapter


class Database(object):

    def __init__(self, database: IDatabaseAdapter, track_factory: TrackFactory):
        self.db = database
        self.trackFactory = track_factory

    def refreshDB(self) -> None:
        return NotImplemented

    def addTrack(
            self,
            location: str,
            title: str=None,
            artist: str=None,
            album: str=None,
            track_type: str=None,
            **kwargs
    ) -> None:
        self.db.addTrack(location, title, artist, album, track_type, **kwargs)

    def getTracks(self) -> List[Track]:
        track_dicts = self.db.getTracks()
        return [self.trackFactory.getTrack(**track_dict) for track_dict in track_dicts]

    def getArtists(self) -> List[str]:
        return self.db.getArtists()

    def getAlbums(self) -> List[str]:
        return self.db.getAlbums()

    def getAlbumsByArtist(self, artist: str) -> List[str]:
        return self.db.getAlbumsByArtist(artist)

    def getTracksByArtist(self, artist: str) -> List[Track]:
        track_dicts = self.db.getTracksByArtist(artist)
        return [self.trackFactory.getTrack(**track_dict) for track_dict in track_dicts]

    def getTracksByAlbum(self, artist: str, album: str) -> List[Track]:
        track_dicts = self.db.getTracksByAlbum(artist, album)
        return [self.trackFactory.getTrack(**track_dict) for track_dict in track_dicts]

    def getTrack(self, title: str, artist: str, album: str) -> Track:
        return self.trackFactory.getTrack(**self.db.getTrack(title, artist, album))

    def getUnimported(self) -> List[Track]:
        track_dicts = self.db.getUnimported()
        return [self.trackFactory.getTrack(**track_dict) for track_dict in track_dicts]

    def getUnavailable(self) -> List[Track]:
        track_dicts = self.db.getUnavailable()
        return [self.trackFactory.getTrack(**track_dict) for track_dict in track_dicts]


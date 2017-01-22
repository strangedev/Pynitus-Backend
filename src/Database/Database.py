"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List, Dict

from src.Config.ConfigLoader import ConfigLoader
from src.Data.Tagging import TagReader
from src.Data.Tagging import TagSupport
from src.Data.Tagging.TagSupport import TagValue
from src.Data.Track.Track import Track
from src.Data.Track.TrackFactory import TrackFactory
from src.Database.IDatabaseAdapter import IDatabaseAdapter
from src.Utilities import MediaScanner
from src.Utilities.TypingFixes import Maybe


class Database(object):

    adapter = None

    @classmethod
    def setDatabaseAdapter(cls, adapter: IDatabaseAdapter.__class__):
        cls.adapter = adapter

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.db = Database.adapter(self.config.get("db_path"))  # type: IDatabaseAdapter
        self.trackFactory = TrackFactory(self.db)

        self.refreshDB()

    def refreshDB(self) -> None:
        self.db.setAllUninitialized()
        self.db.setAllUnavailable()

        # Get all local files
        for file_path in MediaScanner.iterateAudioFiles(self.config.get("musicDirectory")):
            add_track = True
            tag_info = TagReader.readTag(file_path)
            required_metadata_present = all([bool(tag_info[key]) for key in TagSupport.REQUIRED_TAGS])

            if required_metadata_present:
                # Check if exists in db
                if self.db.getByLocation(file_path) is not None:
                    add_track = False

            if add_track:
                self.addTrack(
                    file_path,
                    "FileTrack",
                    tag_info
                )

            self.db.setTrackIsAvailable(file_path)
            self.db.setTrackIsInitialized(file_path)

        # Check remaining uninitialized tracks
        for track in (self.trackFactory.getTrack(**td) for td in self.db.getUninitialized()):
            print(track)
            if track.available():
                self.db.setTrackIsAvailable(track.location)
            self.db.setTrackIsInitialized(track.location)

    def addTrack(
            self,
            location: str,
            track_type: str,
            tag_info: Dict[str, TagValue]
    ) -> None:
        self.db.addTrack(location, track_type, tag_info)

    def getByLocation(self, location: str) -> Maybe(Track):
        """
        Returns a track by it's location, doesn't mind whether it's imported or not.
        :param location: The tracks location
        :return: The track if found, None otherwise
        """
        track_dict = self.db.getByLocation(location)
        if track_dict is None:
            return None
        return self.trackFactory.getTrack(**track_dict)

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

    def updateTrack(self, track) -> None:
        for internal_name in TagSupport.REQUIRED_TAGS:
            if internal_name not in track.tag_info:
                return
            if track.tag_info[internal_name] is None or track.tag_info[internal_name] == []:
                return

        self.db.updateTrack(track.location, track.tag_info)

    def importTrack(self, track):
        self.db.setTrackIsImported(track.location)
        self.db.setTrackIsAvailable(track.available())
        self.db.setTrackIsInitialized(track.location)


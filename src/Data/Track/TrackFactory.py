"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

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
from typing import Dict

from src.Data.Tagging import TagSupport
from src.Data.Track.Track import Track
from src.Data.Foundation.UniqueFactory import UniqueFactory
from src.Database.IDatabaseAdapter import IDatabaseAdapter


class TrackFactory(UniqueFactory):

    track_types = dict({"FileTrack": Track})  # type:Dict[str, Track.__class__]

    @classmethod
    def register(cls, track_type, constructor):
        cls.track_types[track_type] = constructor

    def __init__(self, database: IDatabaseAdapter):
        super(TrackFactory, self).__init__(Track, "title", "artist", "album")

        self.db = database

    def getTrack(self, **kwargs):

        self.setConstructor(TrackFactory.track_types[kwargs["type"]])

        track = self.new(
            title=kwargs["title"],
            artist=kwargs["artist"],
            album=kwargs["album"]
        )

        for key in set(kwargs) - {"type", "title", "artist", "album"}:
            setattr(track, key, kwargs[key])

        self.generateMetadataHook(track)
        return track

    def generateMetadataHook(self, track):

        meta_data = self.db.getMetainformation(track.title, track.artist, track.album)

        for key in TagSupport.TAGLIB_INTERNAL_NAMES.values():
            setattr(track, "__" + key, None)

        if meta_data is None:
            return

        for key in meta_data:
            setattr(track, "__" + key, meta_data[key])

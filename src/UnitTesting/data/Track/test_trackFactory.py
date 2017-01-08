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

from unittest import TestCase
from unittest.mock import MagicMock

from src.Data.Track.TrackFactory import TrackFactory


class TestTrackFactory(TestCase):
    def test_register(self):
        constructor = MagicMock(return_value="foo")

        TrackFactory.register("bar", constructor)

        self.assertIn("bar", TrackFactory.track_types, "New track type couldn't be registered")

    def test_getTrack(self):
        track = MagicMock(name="track")
        constructor = MagicMock(return_value=track)
        database = MagicMock()
        database.getMetainformation = MagicMock(return_value={"publisher": "peter lustig"})

        TrackFactory.register("foo", constructor)
        factory = TrackFactory(database)

        track = factory.getTrack(type="foo", title="a", artist="b", album="c", direct="f")
        self.assertEquals(track.direct, "f")

        constructor.assert_called_once_with(title="a", artist="b", album="c")

    def test_loadMetadata(self):
        track = MagicMock(name="track")
        track.title = "a"
        track.artist = "b"
        track.album = "c"
        constructor = MagicMock(return_value=track)
        database = MagicMock()
        database.getMetainformation = MagicMock(return_value={"publisher": "peter lustig"})

        TrackFactory.register("foo", constructor)
        factory = TrackFactory(database)

        factory.loadMetadata(track)

        self.assertEquals(track.publisher, "peter lustig")
        database.getMetainformation.assert_called_once_with("a", "b", "c")

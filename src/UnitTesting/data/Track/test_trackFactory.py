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

import json

from Pynitus.model import playlists
from Pynitus.model import tracks
from Pynitus.model.db.models import Track, Artist, Album, Playlist


class APIEncoder(json.JSONEncoder):

    encodes_class = None

    def __init__(self, no_data=False):
        super().__init__()
        self.__no_data = no_data

    def default(self, o):
        if isinstance(o, self.encodes_class):
            r = self.encode_metadata(o)

            if self.__no_data:
                return r

            r['data'] = self.encode_data(o)
            return r

        return json.JSONEncoder.default(self, o)

    def encode_metadata(self, o):
        return NotImplemented

    def encode_data(self, o):
        return NotImplemented


class ArtistEncoder(APIEncoder):

    encodes_class = Artist

    def encode_metadata(self, o):
        return {'id': o.id, 'type': 'artist', 'follow': '/artists/id/' + str(o.id)}

    def encode_data(self, o):
        return {'name': o.name}


class AlbumEncoder(APIEncoder):

    encodes_class = Album

    def encode_metadata(self, o):
        return {'id': o.id, 'type': 'album', 'follow': '/albums/id/' + str(o.id)}

    def encode_data(self, o):
        return {
            'title': o.title,
            'artist': ArtistEncoder().default(o.artist)
        }


class TrackEncoder(APIEncoder):

    encodes_class = Track

    def encode_metadata(self, o):
        return {'id': o.id, 'type': 'track', 'follow': '/tracks/id/' + str(o.id)}

    def encode_data(self, o):
        return {
            'artist': ArtistEncoder().default(o.artist),
            'album': AlbumEncoder().default(o.album),
            'title': o.title
        }


class DetailedTrackEncoder(APIEncoder):

    encodes_class = Track

    def encode_metadata(self, o):
        return {'id': o.id, 'type': 'track', 'follow': '/tracks/id/' + str(o.id)}

    def encode_data(self, o):
        return {
            'artist': ArtistEncoder().default(o.artist),
            'album': AlbumEncoder().default(o.album),
            'title': o.title
            # TODO: tag info
        }


class PlaylistEncoder(APIEncoder):

    encode_class = Playlist

    def encode_metadata(self, o):
        return {'id': o.id, 'type': 'playlist', 'follow': '/playlists/id/' + str(o.id)}

    def encode_data(self, o: Playlist):
        track_encoder = TrackEncoder()
        return {
            'name': o.name,
            'username': o.username,
            'tracks': [track_encoder.default(track) for track in tracks.on_playlist(o.id)]
        }

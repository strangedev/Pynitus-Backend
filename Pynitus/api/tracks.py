from flask import request

from Pynitus import app
from Pynitus.api.encoders import TrackEncoder
from Pynitus.api.request_util import expect_optional

from Pynitus.model import tracks


@app.route('/tracks/all', methods=['GET'])
@expect_optional([('offset', int), ('amount', int)])
def tracks_all(offset=0, amount=0):
    return TrackEncoder().encode(tracks.all(offset=offset, limit=amount))


@app.route('/tracks/unimported', methods=['GET'])
@expect_optional([('offset', int), ('amount', int)])
def tracks_unimported(offset=0, amount=0):
    return TrackEncoder().encode(tracks.unimported(offset=offset, limit=amount))


@app.route('/tracks/unavailable', methods=['GET'])
@expect_optional([('offset', int), ('amount', int)])
def tracks_unavailable(offset=0, amount=0):
    return TrackEncoder().encode(tracks.unavailable(offset=offset, limit=amount))


@app.route('/tracks/album/<int:album_id>', methods=['GET'])
def tracks_album(album_id):
    return TrackEncoder().encode(tracks.on_album(album_id))


@app.route('/tracks/artist/<int:artist_id>', methods=['GET'])
def tracks_artist(artist_id):
    return TrackEncoder().encode(tracks.from_artist(artist_id))


@app.route('/tracks/id/<int:track_id>', methods=['GET'])
def tracks_id(track_id):
    return TrackEncoder().encode(tracks.get(track_id))

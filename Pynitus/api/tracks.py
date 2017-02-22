from flask import request

from Pynitus import app
from Pynitus.api.encoders import TrackEncoder

from Pynitus.model import tracks


@app.route('/tracks/all', methods=['GET'])
def all():
    start = request.args.get('start')
    amount = request.args.get('amount')

    if start is None or not type(start) == int:
        start = 0

    if amount is None or not type(amount) == int:
        amount = 0

    return TrackEncoder().encode(tracks.all(starting_with=start, limit=amount))


@app.route('/tracks/unimported', methods=['GET'])
def unimported():
    start = request.args.get('start')
    amount = request.args.get('amount')

    if start is None or not type(start) == int:
        start = 0

    if amount is None or not type(amount) == int:
        amount = 0

    return TrackEncoder().encode(tracks.unimported(starting_with=start, limit=amount))


@app.route('/tracks/unavailable', methods=['GET'])
def unavailable():
    start = request.args.get('start')
    amount = request.args.get('amount')

    if start is None or not type(start) == int:
        start = 0

    if amount is None or not type(amount) == int:
        amount = 0

    return TrackEncoder().encode(tracks.unavailable(starting_with=start, limit=amount))


@app.route('/tracks/album/<int:album_id>', methods=['GET'])
def album(album_id):
    return TrackEncoder().encode(tracks.on_album(album_id))


@app.route('/tracks/artist/<int:artist_id>', methods=['GET'])
def artist(artist_id):
    return TrackEncoder().encode(tracks.from_artist(artist_id))


@app.route('/tracks/id/<int:track_id>', methods=['GET'])
def id(track_id):
    return TrackEncoder().encode(tracks.get(track_id))

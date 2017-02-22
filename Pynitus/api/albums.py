from flask import request

from Pynitus import app
from Pynitus.api.encoders import AlbumEncoder
from Pynitus.model import albums


@app.route('/albums/all', methods=['GET'])
def albums_all():
    start = request.args.get('start')
    amount = request.args.get('amount')

    if start is None or not type(start) == int:
        start = 0

    if amount is None or not type(amount) == int:
        amount = 0

    return AlbumEncoder().encode(albums.all(starting_with=start, limit=amount))


@app.route('/albums/artist/<int:artist_id>', methods=['GET'])
def albums_artist(artist_id):
    return AlbumEncoder().encode(albums.from_artist(artist_id))


@app.route('/albums/id/<int:album_id>', methods=['GET'])
def albums_id(album_id):
    return AlbumEncoder().encode(albums.get(album_id))

from flask import request

from Pynitus import app
from Pynitus.api.encoders import ArtistEncoder
from Pynitus.model import artists


@app.route('/artists/all', methods=['GET'])
def artists_all():
    start = request.args.get('start')
    amount = request.args.get('amount')

    if start is None or not type(start) == int:
        start = 0

    if amount is None or not type(amount) == int:
        amount = 0

    return ArtistEncoder().encode(artists.all(starting_with=start, limit=amount))


@app.route('/artists/id/<int:artist_id>', methods=['GET'])
def artists_id(artist_id):
    return ArtistEncoder().encode(artists.get(artist_id))

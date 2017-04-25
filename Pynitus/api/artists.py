from Pynitus import app
from Pynitus.api.encoders import ArtistEncoder
from Pynitus.api.request_util import expect_optional
from Pynitus.model import artists


@app.route('/artists/all', methods=['GET'])
@expect_optional(('offset', int), ('amount', int))
def artists_all(offset=0, amount=0):
    return ArtistEncoder().encode(artists.all(offset=offset, limit=amount))


@app.route('/artists/id/<int:artist_id>', methods=['GET'])
def artists_id(artist_id):
    return ArtistEncoder().encode(artists.get(artist_id))

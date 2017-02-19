from Pynitus import app
from Pynitus.api.encoders import TrackEncoder

from Pynitus.model import tracks


@app.route('/tracks/all/<int:start>/<int:amount>', methods=['GET'])
def all(start, amount):
    return TrackEncoder().encode(tracks.all(starting_with=start, limit=amount))


@app.route('/tracks/unimported/<int:start>/<int:amount>', methods=['GET'])
def unimported(start, amount):
    return TrackEncoder().encode(tracks.unimported(starting_with=start, limit=amount))


@app.route('/tracks/unavailable/<int:start>/<int:amount>', methods=['GET'])
def unavailable(start, amount):
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

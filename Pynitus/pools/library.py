from typing import List

from sqlalchemy import desc, asc

from Pynitus.model.database import db_session
from Pynitus.model.models import Artist, Album, Track


def __non_hidden_tracks():
    return db_session.query(Track).join(Track.status).filter(Track.hidden is False)


def tracks(starting_with: int=0, limit: int=0, sorted_by: str="title", sort_order: str="asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param starting_with: The id of the track to start from
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = __non_hidden_tracks()

    if starting_with > 0:
        starting_with += 1
        q = q.filter(Track.id >= starting_with)

    order_by_column = Track.title if sorted_by == "title" else Track.artist if sorted_by == "artist" else Track.album

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def on_album(album_id: int) -> List[Track]:

    album = db_session.query(Album).get(album_id)

    if not album:
        return []

    return [t for t in album.tracks if not t.hidden]


def from_artist(artist_id: int) -> List[Track]:

    artist = db_session.query(Artist).get(artist_id)

    if not artist:
        return []

    return [t for t in artist.tracks if not t.hidden]


def add():
    pass


def update():
    pass


def delete():
    pass


def show():
    pass


def hide():
    pass


def get(track_id: int) -> Track:
    pass

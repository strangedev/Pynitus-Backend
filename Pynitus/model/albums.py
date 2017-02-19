from typing import List

from sqlalchemy import asc
from sqlalchemy import desc

from Pynitus.model.database import db_session, persistance
from Pynitus.model.models import Album, Track, Status
from Pynitus.model import artists


def all(starting_with: int=0, limit: int=0, sorted_by: str="title", sort_order: str="asc") -> List[Album]:
    """
    Returns all albums with one or more non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist)
    :param starting_with: The id of the album to start from
    :param limit: The number of albums to return
    :return: All albums with one or more non hidden tracks in the database
    """

    q = db_session.query(Album)\
        .join(Track)\
        .join(Track.status)\
        .filter(Status.imported == True) \
        .filter(Status.available == True) \
        .group_by(Album.id)

    if starting_with > 0:
        q = q.filter(Album.id >= starting_with)

    order_by_column = Album.title if sorted_by == "title" else Album.artist

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def from_artist(artist_id: int) -> List[Album]:

    artist = artists.get(artist_id)

    if artist is None:
        return []

    return artist.albums


def get_or_create(title: str, artist: str) -> Album:

    a = artists.get_or_create(artist)

    album = db_session.query(Album)\
        .filter(Album.title == title)\
        .filter(Album.artist == a) \
        .first()

    if album is None:
        with persistance():
            album = Album(title=title)
            album.artist = a
            db_session.add(album)

    return album


def get(album_id: int) -> Album:

    return db_session.query(Album).get(album_id)

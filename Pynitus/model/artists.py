from typing import List

from sqlalchemy import asc
from sqlalchemy import desc

from Pynitus.model.db.database import db_session, persistance
from Pynitus.model.db.models import Artist, Track, Status


def all(starting_with: int=0, limit: int=0, sorted_by: str="name", sort_order: str="asc") -> List[Artist]:
    """
    Returns all artists with one or more non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist)
    :param starting_with: The id of the artist to start from
    :param limit: The number of artists to return
    :return: All artists with one or more non hidden tracks in the database
    """

    q = db_session.query(Artist)\
        .join(Track)\
        .join(Track.status)\
        .filter(Status.imported == True) \
        .filter(Status.available == True) \
        .group_by(Artist.id)

    if starting_with > 0:
        q = q.filter(Artist.id >= starting_with)

    order_by_column = Artist.name if sorted_by == "name" else Artist.artist

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def get_or_create(name: str) -> Artist:

    artist = db_session.query(Artist).filter(Artist.name == name).first()

    if artist is None:
        with persistance():
            artist = Artist(name=name)
            db_session.add(artist)

    return artist


def get(artist_id: int) -> Artist:
    return db_session.query(Artist).get(artist_id)

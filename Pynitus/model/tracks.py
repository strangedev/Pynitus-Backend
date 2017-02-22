from typing import List

from Pynitus.model.db.database import db_session, persistance
from sqlalchemy import desc, asc

from Pynitus.model import albums, artists
from Pynitus.model.db.models import Track, Status


def all(starting_with: int=0, limit: int=0, sorted_by: str="title", sort_order: str="asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param starting_with: The id of the track to start from
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = db_session.query(Track)\
        .join(Track.status)\
        .filter(Status.imported == True)\
        .filter(Status.available == True)

    if starting_with > 0:
        q = q.filter(Track.id >= starting_with)

    order_by_column = Track.title if sorted_by == "title" else Track.artist if sorted_by == "artist" else Track.album

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def unimported(starting_with: int=0, limit: int=0, sorted_by: str="title", sort_order: str="asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param starting_with: The id of the track to start from
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = db_session.query(Track)\
        .join(Track.status)\
        .filter(Status.imported == False)

    if starting_with > 0:
        q = q.filter(Track.id >= starting_with)

    order_by_column = Track.title if sorted_by == "title" else Track.artist if sorted_by == "artist" else Track.album

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def unavailable(starting_with: int=0, limit: int=0, sorted_by: str="title", sort_order: str="asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param starting_with: The id of the track to start from
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = db_session.query(Track)\
        .join(Track.status)\
        .filter(Status.imported == True)\
        .filter(Status.available == False)

    if starting_with > 0:
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
    """
    Gets all tracks on a specific album
    :param album_id:
    :return:
    """

    album = albums.get(album_id)

    print(album)
    print(album.tracks[0].status.available)

    if album is None:
        return []

    return [t for t in album.tracks if t.status.available and t.status.imported]


def from_artist(artist_id: int) -> List[Track]:

    artist = artists.get(artist_id)

    if artist is None:
        return []

    return [t for t in artist.tracks if t.status.available and t.status.imported]


def get(track_id: int) -> Track:

    return db_session.query(Track).get(track_id)


def get_or_create(title: str, artist: str, album: str) -> Track:

    a = albums.get_or_create(album, artist)

    t = db_session.query(Track)\
        .filter(Track.title == title)\
        .filter(Track.album == a)\
        .filter(Track.artist == a.artist)\
        .first()

    if t is None:
        with persistance():
            t = Track(title=title)
            t.album = a
            t.artist = t.album.artist
            db_session.add(t)

    if t.status is None:
        with persistance():
            s = Status(t)
            db_session.add(s)

    return t


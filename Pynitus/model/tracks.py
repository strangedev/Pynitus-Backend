from typing import List

from Pynitus.model.db.database import db_session, persistance
from sqlalchemy import desc, asc

from Pynitus.model import albums, artists
from Pynitus.model.db.models import Track, Album, Artist, Status, PlaylistTrack


def all(offset: int=0, limit: int=0, sorted_by: str= "title", sort_order: str= "asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param offset: How many tracks to omit from the beginning of the result
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = db_session.query(Track)\
        .join(Track.status)\
        .filter(Status.imported == True)\
        .filter(Status.available == True)

    if sorted_by == "title":
        order_by_column = Track.title
    elif sorted_by == "artist":
        order_by_column = Track.artist
    else:
        order_by_column = Track.album

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if offset > 0:
        q = q.offset(offset)

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def unimported(offset: int=0, limit: int=0, sorted_by: str= "title", sort_order: str= "asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param offset: How many tracks to omit from the beginning of the result
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = db_session.query(Track)\
        .join(Track.status)\
        .filter(Status.imported == False)

    if sorted_by == "title":
        order_by_column = Track.title
    elif sorted_by == "artist":
        order_by_column = Track.artist
    else:
        order_by_column = Track.album

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if offset > 0:
        q = q.offset(offset)

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def unavailable(offset: int=0, limit: int=0, sorted_by: str= "title", sort_order: str= "asc") -> List[Track]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (title, artist, album)
    :param offset: How many tracks to omit from the beginning of the result
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """

    q = db_session.query(Track)\
        .join(Track.status)\
        .filter(Status.imported == True)\
        .filter(Status.available == False)

    if sorted_by == "title":
        order_by_column = Track.title
    elif sorted_by == "artist":
        order_by_column = Track.artist
    else:
        order_by_column = Track.album

    if sort_order == "desc":
        q = q.order_by(desc(order_by_column))
    else:
        q = q.order_by(asc(order_by_column))

    if offset > 0:
        q = q.offset(offset)

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


def exists(title: str, artist: str, album: str) -> bool:

    t = db_session.query(Track) \
        .join(Artist) \
        .join(Album) \
        .filter(Track.title == title) \
        .filter(Album.title == album) \
        .filter(Artist.name == artist) \
        .first()

    return t is not None


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


def get_tracks_on_playlist(playlist_id: int) -> List[Track]:
    """
    gets List of Tracks to given playlist_id
    :param playlist_id: int to identify Playlist to get Tracks of
    :return: List of Tracks from Playlist
    """
    tracks = []
    q = db_session.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).all()
    for p_track in q:
        tracks.append(p_track.track)
    return tracks

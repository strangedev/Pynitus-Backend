from typing import List

from sqlalchemy import asc
from sqlalchemy import desc

from Pynitus import db_session
from Pynitus.model.db.database import persistance
from Pynitus.model.db.models import Playlist, User, PlaylistTracks


def all(offset: int = 0, limit: int = 0, sorted_by: str = "id", sort_order: str = "asc") -> List[Playlist]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (id, playlist_name, user_name, user_id)
    :param offset: The e.g. id of the track to start from
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """
    q = db_session.query(Playlist)

    if sorted_by == "id":
        col_order = Playlist.id
    elif sorted_by == "playlist_name":
        col_order = Playlist.name
    elif sorted_by == "user_name":
        col_order = Playlist.user
    else:
        col_order = Playlist.user_id

    if sort_order == "desc":
        q = q.order_by(desc(col_order))
    else:
        q = q.order_by(asc(col_order))

    if offset > 0:
        q = q.offset(offset)

    if limit > 0:
        q = q.limit(limit)

    return q.all()


def get(p_id: int):
    """

    :param p_id: Unique Id of Playlist to get.
    :return: Playlist
    """
    return db_session.query(Playlist).get(p_id)


def from_user(username: str) -> List[Playlist]:
    """

    :param username: name of User to get List of Playlist from.
    :return: List of Playlist
    """
    # TODO switch to User_id
    user_id = db_session.query(User).filter(User.username == username)
    playlist = get(user_id)

    if playlist is None:
        return []

    return [p for p in playlist]


def create(username: str, playlist_name: str, track_id: int) -> Playlist:
    """
    Sollten
    Die Playlist erstellen, add_track aufrufen.
    add_track via PlaylistId?,
    :param username: String
    :param playlist_name: String
    :param track_id:
    :return:
    """
    with persistance():
        playlist_track = PlaylistTracks(track_id=track_id)
        playlist = Playlist(user_id=username, name=playlist_name)
        playlist_track.playlist = playlist
        db_session.add(playlist)
    return playlist


def add_track(playlist_id: int, track_id: int) -> Playlist:
    """
    Add Track by id in Playlist by id
    :param playlist_id:
    :param track_id:
    :return:
    """
    playlist = get(playlist_id)
    with persistance():
        playlist_tracks = PlaylistTracks(track_id=track_id)
        playlist_tracks.playlist = playlist
        db_session.add(playlist_tracks)
    return playlist_tracks.playlist


def remove_track(playlist_id: int, track_id: int) -> bool:
    """
    removes Track by id in Playlist by id
    :param playlist_id: unique int of Playlist to remove
    :param track_id: unique int of track to remove
    :return: succeed?
    """
    playlist_track = db_session.query(PlaylistTracks). \
        filter(PlaylistTracks.playlist_id == playlist_id). \
        filter(PlaylistTracks.track_id == track_id).first()
    print(playlist_track)
    if playlist_track is None:
        return False

    with persistance():
        db_session.query(PlaylistTracks).filter(PlaylistTracks.id == playlist_track.id).delete()
    return True


def remove(playlist_id: int) -> bool:
    """
    removes Playlist by given playlist_id
    :param playlist_id: unique int of Playlist to remove
    :return: succeed?
    """
    with persistance():
        db_session.query(Playlist).filter(Playlist.id == playlist_id).delete()
    return True


def fusion(playlist_id_1: int, playlist_id_2: int, mode: str = "normal", name: str="mixed") -> Playlist:
    """
    creates new Playlist, based on given playlist_id_1, _id_2
    :param playlist_id_1: starting playlist in normal mode
    :param playlist_id_2: upcoming playlist in normal mode
    :param mode: normal(default) returns a Playlist starting with playlist_id_1 then playlist_id_2,
                merge_'x' returns Playlist merged by x, where x can be album, artist, id, title,
                TODO: could be the same? randomized, shuffle
    :return:
    """
    if mode == "normal":
        playlist = db_session.query(PlaylistTracks) \
            .filter((PlaylistTracks.playlist_id == playlist_id_1) \
                    or (PlaylistTracks.playlist_id == playlist_id_2)).all()
        temp = playlist.pop()
        p = create(temp.playlist.user_id, name, temp.track_id)

        for e in playlist:
            add_track(p.id, e.track_id)
        return p
    elif mode.startswith("merge_"):
        # TODO: implement
        return None
    elif mode == "randomize":
        # TODO: implement
        return None
    elif mode == "shuffle":
        # TODO: implement
        return None
    else:
        return None

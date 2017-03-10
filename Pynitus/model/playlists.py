"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Vivian Peter Franz
    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List

from sqlalchemy import asc
from sqlalchemy import desc

from Pynitus import db_session
from Pynitus.model.db.database import persistance
from Pynitus.model.db.models import Playlist, User, PlaylistTrack


def all(offset: int = 0, limit: int = 0, sorted_by: str = "id", sort_order: str = "asc") -> List[Playlist]:
    """
    Returns all non hidden tracks in the database
    :param sort_order: Whether to sort "asc"ending or "desc"ending
    :param sorted_by: By which attribute to sort (id, playlist_name, user_name, username)
    :param offset: The e.g. id of the track to start from
    :param limit: The number of tracks to return
    :return: All non hidden tracks in the database
    """
    q = db_session.query(Playlist)

    if sorted_by == "id":
        col_order = Playlist.id
    elif sorted_by == "playlist_name":
        col_order = Playlist.name
    elif sorted_by == "username":
        col_order = Playlist.user
    else:
        col_order = Playlist.username

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
    playlist = db_session.query(Playlist).filter(Playlist.username == username).all()

    if playlist is None:
        return []

    return [p for p in playlist]


def create(username: str, playlist_name: str) -> Playlist:
    """
    :param username: String
    :param playlist_name: String
    :param track_id:
    :return:
    """
    with persistance():
        playlist = Playlist(user_id=username, name=playlist_name)
        db_session.add(playlist)
    return playlist


def add_track(playlist_id: int, track_id: int) -> bool:
    """
    Add Track by id in Playlist by id
    :param playlist_id:
    :param track_id:
    :return:
    """
    # TODO: Check if get returns None
    playlist = get(playlist_id)
    with persistance():
        playlist_tracks = PlaylistTrack(track_id=track_id)
        playlist_tracks.playlist = playlist
        db_session.add(playlist_tracks)
    return True


def remove_track(playlist_id: int, track_id: int) -> bool:
    """
    removes Track by id in Playlist by id
    :param playlist_id: unique int of Playlist to remove
    :param track_id: unique int of track to remove
    :return: succeed?
    """
    playlist_track = db_session.query(PlaylistTrack). \
        filter(PlaylistTrack.playlist_id == playlist_id). \
        filter(PlaylistTrack.track_id == track_id).first()
    if playlist_track is None:
        return False

    with persistance():
        db_session.query(PlaylistTrack).filter(PlaylistTrack.id == playlist_track.id).\
                filter(PlaylistTrack.track_id == track_id).delete()
    return True


def remove(playlist_id: int) -> bool:
    """
    removes Playlist by given playlist_id
    :param playlist_id: unique int of Playlist to remove
    :return: succeed?
    """
    playlist = db_session.query(Playlist).filter(Playlist.id == playlist_id)
    if playlist is None:
        return False
    else:
        with persistance():
            db_session.query(Playlist).filter(Playlist.id == playlist_id).delete()
        return True

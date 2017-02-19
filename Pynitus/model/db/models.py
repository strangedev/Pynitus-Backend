from sqlalchemy import Column, Integer, Boolean, LargeBinary, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from Pynitus.model.db.database import Base


# TODO: http://docs.sqlalchemy.org/en/latest/orm/cascades.html


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship(Artist, backref=backref('albums', uselist=True))

class TagInfo(Base):
    __tablename__ = "taginfo"

    id = Column(Integer, primary_key=True)
    # TODO: add tag fields


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship(Artist, backref=backref('tracks', uselist=True))
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship(Album, backref=backref('tracks', uselist=True))
    title = Column(String(256))
    mrl = Column(String(1024))


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship(Track, backref=backref('status', uselist=False))
    imported = Column(Boolean)
    available = Column(Boolean)
    backend = Column(String(128))

    def __init__(self, track: Track):
        self.imported = False
        self.available = False
        self.resource_type = "local"
        self.track = track


class User(Base):
    __tablename__ = 'user'

    username = Column(String(128), primary_key=True)
    password_hash = Column(LargeBinary)
    password_salt = Column(LargeBinary)
    privilege_level = Column(Integer)


class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), ForeignKey('user.username'))
    user = relationship(User, backref=backref('playlists', uselist=True))
    name = Column(String(1024))


class PlaylistTracks(Base):
    __tablename__ = 'playlist_tracks'

    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlist.id'))
    playlist = relationship(Playlist, backref=backref('tracks', uselist=True))
    track_id = Column(Integer, ForeignKey('track.id'))

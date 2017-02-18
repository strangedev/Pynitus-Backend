from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# TODO: http://docs.sqlalchemy.org/en/latest/orm/cascades.html


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    title = Column(String(256))


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship('Track', backref=backref('status', uselist=False))
    imported = Column(Boolean)
    available = Column(Boolean)
    resource_type = Column(String(128))


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship(Artist, backref=backref('tracks', uselist=True))
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship(Album, backref=backref('tracks', uselist=True))
    title = Column(String(256))
    mrl = Column(String(1024))

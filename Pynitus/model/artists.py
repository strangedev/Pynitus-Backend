from Pynitus.model.db.database import db_session, persistance

from Pynitus.model.db.models import Artist


def get_or_create(name: str) -> Artist:

    artist = db_session.query(Artist).filter(Artist.name == name).first()

    if artist is None:
        with persistance():
            artist = Artist(name=name)
            db_session.add(artist)

    return artist

def get(artist_id: int) -> Artist:
    return db_session.query(Artist).get(artist_id)

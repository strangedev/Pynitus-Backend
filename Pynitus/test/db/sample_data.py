import os

from Pynitus import init_db
from Pynitus.model import tracks
from Pynitus.model.db.database import db_session, persistance


def generate_sample_tracks(n: int=10000):

    import Pynitus.model.db.database
    init_db()

    for i in range(n):

        random_title = os.urandom(32).hex()
        random_album_title = os.urandom(32).hex()
        random_artist_name = os.urandom(32).hex()

        t = tracks.get_or_create(random_title, random_artist_name, random_album_title)

        with persistance():
            t.status.available = True
            t.status.imported = True
            t.backend = "vlc_backend"
            t.mrl = "test.mp3"

    db_session.close()
    db_session.remove()


if __name__ == "__main__":
    generate_sample_tracks(1000)

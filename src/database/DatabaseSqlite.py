from typing import List, Dict

import sqlite3

from src.database.DatabaseAdapter import DatabaseAdapter


class DatabaseSqlite(DatabaseAdapter):
    def __init__(
            self,
            db_path: str):
        """
        :param db_path: Location where to Store DB
        """
        self.db = sqlite3.connect(db_path)  # type: sqlite3.Connection
        try:
            self.db.execute("CREATE TABLE " + "track(" +
                            "title text, " +
                            "artist text, " +
                            "album text, " +
                            "location text primary key, " +
                            "imported bool, " +
                            "available bool, " +
                            "type text, " +
                            "init bool)")
        except sqlite3.OperationalError as e:
            print(e)

        try:
            self.db.execute("CREATE TABLE " + "involved(" +
                            "location text, " +
                            "feature text)")
        except sqlite3.OperationalError as e:
            print(e)

        try:
            self.db.execute("CREATE TABLE " + "genres(" +
                            "location text, " +
                            "genre text)")
        except sqlite3.OperationalError as e:
            print(e)
        self._t_nfo = ["location", "subtitle text", "additional_artist1", "additional_artist2",
                       "additional_artist3", "composer", "lyricist", "publisher", "year", "track_number", "bpm", "key",
                       "mood", "length", "lyrics", "artist_url", "publisher_url", "file_type",
                       "user_comment"]  # type [str]  FIXME: Get from ID3Standard.py
        a = self._t_nfo
        try:
            ex_cmd = "CREATE TABLE trackTag(" + a[0] + "text primary key, "
            for i in range(1,18):
                ex_cmd += a[i] + "text, "
            ex_cmd += a[18] + "text)"
            self.db.execute(ex_cmd)
        except sqlite3.OperationalError as e:
            print(e)

        self.__setAllUnavailable()
        self.__setAllUnimported()
        self.__setAllUninitialized()

    def getTrack(self, title: str, artist: str, album: str) -> Dict[str, any]:
        """
        :param title: Title from Track to get
        :param artist: Artist from Track to get
        :param album: Album from Track to get
        :return: Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
        """
        # FIXME: escape input strings
        track_tuple = self.db.execute("SELECT * FROM track WHERE title = ? AND artist = ? AND album = ?",
                                      [title, artist, album])
        t = track_tuple.fetchone()
        if t is None:
            return None
        track = {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": bool(t[4]),
                 "available": bool(t[5]), "type": t[6], "initialized": t[7]}
        return track

    def getUnimported(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                where imported is 0
        """
        r = []
        for track in self.db.execute("SELECT * FROM track WHERE imported = ?", [False]):
            t = track
            r += [
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6], "initialized": t[7]}
            ]
        return r

    def getUnavailable(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    where available is 0
        """
        r = []
        for track in self.db.execute("SELECT * FROM track WHERE available = ?", [False]):
            t = track
            r += [
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6], "initialized": t[7]}
            ]
        return r

    def getTracksByAlbum(self, artist: str, album: str) -> List[Dict[str, any]]:
        """

        :param artist: Artist of Album to get Tracks from
        :param album: Album to get Tracks from
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    based on given Artist and Album
        """
        # FIXME: escape input strings
        r = []
        for track in self.db.execute(
                "SELECT * FROM track WHERE artist = ? AND album = ?", [artist, album]):  # FIXME: SQL-Inj. possible
            t = track
            r += [
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6], "initialized": t[7]}
            ]
        return r

    def addTrack(self, title: str, artist: str, album: str, format_type: str, location: str, **kwargs) -> None:
        """
        :param title: Track Title
        :param artist: Track Artist
        :param album: Track Album
        :param format_type: Track Type
        :param location: Track Location
        :param kwargs: Additional Track Metainformation
        :return: None
        """
        # TODO: Think of a better way to Handle Exception if location already exists
        # FIXME: escape input strings
        try:
            self.db.execute("INSERT INTO track VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [title, artist, album, location, True, False, format_type, False])
            # Will set Import True, Available False, initialized False   # FIXME: SQL-Inj. possible
        except sqlite3.IntegrityError:
            self.db.execute("DELETE FROM track WHERE location = ?", [location])
            self.db.execute("INSERT INTO track VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [title, artist, album, location, True, False, format_type, False])
            # Will set Import True, Available False, initialized False   # FIXME: SQL-Inj. possible
        self.db.commit()
        self.__addTag(kwargs, location)

    def __addTag(self, tag_dict: dict, location: str) -> None:
        """
        :param tag_dict: Additional Track Metainformation
        :param location: Track Location
        :return: None
        """
        tag_informations = []
        for i in range(0, 19):
            if tag_dict.get(self._t_nfo[i]) is None:  # TODO: Wrong membership test, use more readable style
                tag_informations += [None]
            else:
                tag_informations += [tag_dict.get(self._t_nfo[i])]
        # TODO: Think of a better way to Handle Exception if location already exists
        try:
            self.db.execute("INSERT INTO trackTag VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            tag_informations)
        except sqlite3.IntegrityError:
            self.db.execute("DELETE FROM trackTag WHERE location = ?", [location])
            self.db.execute("DELETE FROM genres WHERE location = ?", [location])
            self.db.execute("DELETE FROM involved WHERE location = ?", [location])
            self.db.execute("INSERT INTO trackTag VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            tag_informations)

        if tag_dict.get("genres") is None:
            self.db.execute("INSERT INTO genres VALUES(?, ?)",
                            [location, None])
        else:
            for gen in tag_dict["genres"]:
                self.db.execute("INSERT INTO genres VALUES(?, ?)", [location, gen])

        if tag_dict.get("involved") is None:
            self.db.execute("INSERT INTO involved VALUES(?, ?)", [location, None])
        else:
            for inv in tag_dict["involved"]:
                self.db.execute("INSERT INTO involved VALUES(?, ?)", [location, inv])
        self.db.commit()

    def getTracksByArtist(self, artist: str) -> List[Dict[str, any]]:
        """
        :param artist: Artist to get Tracks from
        :return: List of Dictionary based on given Artist
        """
        r = []
        for track in self.db.execute("SELECT * FROM track WHERE artist = ?", [artist]):
            t = track
            r += [
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6], "initialized": t[7]}
            ]
        return r

    def getMetainformation(self, title: str, artist: str, album: str) -> Dict[str, any]:
        """
        :param title: Title to get Metainformation from
        :param artist: Artist to get Metainformation from
        :param album: Album to get Metainformation from
        :return: Dictionary with Metainformation based on given Artist, Title and Album
        """
        location = self.getTrack(title, artist, album).get("location")
        if location is None:
            return None
        track_tuple = self.db.execute("SELECT * FROM track WHERE location = ?", [location])
        t = track_tuple.fetchone()
        track = {}
        for i in range(0, 19):
            track[self._t_nfo[i]] = t[i]

        genres = self.db.execute("SELECT * FROM genres WHERE location = ?", [location])
        g = []
        if genres is None:
            track["genres"] = None
        else:
            for genre in genres:
                g += [genre[1]]
            track["genres"] = g

        involved = self.db.execute("SELECT * FROM genres WHERE location = ?", [location])
        names = []
        if involved is None:
            track["involved"] = None
        else:
            for involve_row in involved:
                names += [involve_row[1]]
            track["involved"] = names
        return track

    def __setAllUninitialized(self) -> None:
        """
        sets all Data in Tracks marked as uninitialized
        :return: None
        """
        all_tracks = self.db.execute("SELECT * FROM track").fetchall()
        for track in all_tracks:
            self.db.execute("DELETE FROM track WHERE location = ?", [track[3]])
            self.db.execute("INSERT INTO track VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [track[0], track[1], track[2], track[3], track[4], track[5], track[6], False])
            self.db.commit()

    def __setAllUnimported(self) -> None:
        """
        sets all Data in Tracks marked as unimported
        :return: None
        """
        all_tracks = self.db.execute("SELECT * FROM track").fetchall()
        for track in all_tracks:
            self.db.execute("DELETE FROM track WHERE location = ?", [track[3]])
            self.db.execute("INSERT INTO track VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [track[0], track[1], track[2], track[3], False, track[5], track[6], track[7]])
            self.db.commit()

    def __setAllUnavailable(self) -> None:
        """
        sets all Data in Tracks marked as unavailable
        :return: None
        """
        all_tracks = self.db.execute("SELECT * FROM track").fetchall()
        for track in all_tracks:
            print(track)
            self.db.execute("DELETE FROM track WHERE location = ?", [track[3]])
            self.db.execute("INSERT INTO track VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [track[0], track[1], track[2], track[3], track[4], False, track[6], track[7]])
            self.db.commit()

    def setTrackIsImported(self, location: str) -> None:
        """
        :param location: Key of Track which should marked as Imported
        :return: None
        """
        track = self.db.execute("SELECT * FROM track WHERE location = ?", location)
        t = track.fetchone()
        self.db.execute("DELETE FROM track WHERE location = ?", location)
        self.db.execute("INSERT INTO track VALUES(?,?,?,?,?,?,?,?)", [t[0], t[1], t[2], t[3], True, t[5], t[6], t[7]])
        self.db.commit()

    def setTrackIsInitialized(self, location: str) -> None:
        """
        :param location: Key of Track which should marked as Initialized
        :return: None
        """
        track = self.db.execute("SELECT * FROM track WHERE location = ?", location)
        t = track.fetchone()
        self.db.execute("DELETE FROM track WHERE location = ?", location)
        self.db.execute("INSERT INTO track VALUES(?,?,?,?,?,?,?,?)", [t[0], t[1], t[2], t[3], t[4], t[5], t[6], True])
        self.db.commit()

    def setTrackIsAvailable(self, location: str) -> None:
        """
        :param location: Key of Track which should marked as Available
        :return: None
        """
        track = self.db.execute("SELECT * FROM track WHERE location = ?", location)
        t = track.fetchone()
        self.db.execute("DELETE FROM track WHERE location = ?", location)
        self.db.execute("INSERT INTO track VALUES(?,?,?,?,?,?,?,?)", [t[0], t[1], t[2], t[3], t[4], True, t[6], t[7]])
        self.db.commit()

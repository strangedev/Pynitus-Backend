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
        self.db.execute("CREATE TABLE " + "track(" +
                        "title text, " +
                        "artist text, " +
                        "album text, " +
                        "location text primary key, " +
                        "imported bool, " +
                        "available bool, " +
                        "type text)")  # FIXME: Initialized flag missing, see TODO.md line 15
        self.db.execute("CREATE TABLE" + "involved(" +
                        "location text, " +
                        "feature text)")
        self.db.execute("CREATE TABLE" + "genres(" +
                        "location text, " +
                        "genre text)")
        self._t_nfo = ["location", "subtitle text", "additional_artist1", "additional_artist2",
                       "additional_artist3", "composer", "lyricist", "publisher", "year", "track_number", "bpm", "key",
                       "mood", "length", "lyrics", "artist_url", "publisher_url", "file_type",
                       "user_comment"]  # type [str]  FIXME: Get from ID3Standard.py
        a = self._t_nfo
        self.db.execute("CREATE TABLE" + "trackTag(" +  # TODO: beautify/automate
                        a[0] + " text primary key, " +
                        a[1] + " text, " +
                        a[2] + " text, " +
                        a[3] + " text, " +
                        a[4] + " text, " +
                        a[5] + " text, " +
                        a[6] + " text, " +
                        a[7] + " text, " +
                        a[8] + " text, " +
                        a[9] + " text, " +
                        a[10] + " text, " +
                        a[11] + " text, " +
                        a[12] + " text, " +
                        a[13] + " text, " +
                        a[14] + " text, " +
                        a[15] + " text, " +
                        a[16] + " text, " +
                        a[17] + " text, " +
                        a[18] + " text)")

    def getTrack(self, title: str, artist: str, album: str) -> Dict[str, any]:
        """
        :param title: Title from Track to get
        :param artist: Artist from Track to get
        :param album: Album from Track to get
        :return: Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
        """
        # FIXME: escape input strings
        track_tuple = self.db.execute("SELECT * FROM " + "track " + "WHERE " + "title = " + title +
                                      " AND artist = " + artist + " AND album = " + album)  # FIXME: SQL-Inj. possible
        t = track_tuple.fetchone()
        track = {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": bool(t[4]),
                 "available": bool(t[5]), "type": t[6]}
        return track

    def getUnimported(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                where imported is 0
        """
        r = []
        for track in self.db.execute("SELECT * FROM " + "track " + "WHERE " +
                                     "imported = " + "0"):
            t = track
            r.append(list(
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6]}
            ))
        return r

    def getUnavailable(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    where available is 0
        """
        r = []
        for track in self.db.execute("SELECT * FROM " + "track " + "WHERE " +
                                     "available = " + "0"):
            t = track
            r.append(list(
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6]}
            ))
        return r

    def getTracksByAlbum(self, artist: str, album: str) -> List[Dict[str, str]]:
        """

        :param artist: Artist of Album to get Tracks from
        :param album: Album to get Tracks from
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    based on given Artist and Album
        """
        # FIXME: escape input strings
        r = []
        for track in self.db.execute("SELECT * FROM " + "track " + "WHERE " +
                                     "artist = " + artist + " AND album = " + album):  # FIXME: SQL-Inj. possible
            t = track
            r.append(list(
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6]}
            ))
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
        # FIXME: escape input strings
        self.db.execute("INSERT INTO track(" + title + ", " + artist + ", " + location + ", " + "1, " + "0, "
                        + format_type + ")")  # Will set Import True, Available False   # FIXME: SQL-Inj. possible
        self.__addTag(kwargs, location)

    def __addTag(self, tag_dict: dict, location: str) -> None:
        """
        :param tag_dict: Additional Track Metainformation
        :param location: Track Location
        :return: None
        """
        create_cmd = "INSERT INTO trackTag("
        create_cmd += location + ", "
        for i in range(11, 18):  # TODO: Range 11-18?
            if tag_dict.get(self._t_nfo[i]) is None:  # TODO: Wrong membership test, use more readable style
                create_cmd += " None, "
            else:
                create_cmd += tag_dict.get(self._t_nfo[i]) + ", "

        if tag_dict.get(self._t_nfo[18]) is None:
            create_cmd += " None)"
        else:
            create_cmd += tag_dict.get(self._t_nfo[18]) + ")"
        self.db.execute(create_cmd)

        create_cmd = "INSERT INTO genres("
        if tag_dict["genres"] is None:
            self.db.execute(create_cmd + location + ", None)")  # TODO: Same logic as in line 141, reuse
        else:
            for i in range(0, len(tag_dict["genres"])):
                self.db.execute(create_cmd + location + ", " + tag_dict["genres"][i] + ")")

        create_cmd = "INSERT INTO involved("
        if tag_dict["involved"] is None:
            self.db.execute(create_cmd + location + ", None)")
        else:
            for i in range(0, len(tag_dict["involved"])):
                self.db.execute(create_cmd + location + ", " + tag_dict["involved"][i] + ")")

    def getTracksByArtist(self, artist: str) -> List[Dict[str, str]]:
        """
        :param artist: Artist to get Tracks from
        :return: List of Dictionary based on given Artist
        """
        r = []
        for track in self.db.execute("SELECT * FROM " + "track " + "WHERE " +
                                     "artist = " + artist):
            t = track
            r.append(list(
                {"title": t[0], "artist": t[1], "album": t[2], "location": t[3], "imported": t[4],
                 "available": t[5], "type": t[6]}
            ))
        return r

    def getMetainformation(self, title: str, artist: str, album: str) -> Dict[str, str]:
        """
        :param title: Title to get Metainformation from
        :param artist: Artist to get Metainformation from
        :param album: Album to get Metainformation from
        :return: Dictionary with Metainformation based on given Artist, Title and Album
        """
        location = self.getTrack(title, artist, album).get("location")
        if location is None:
            return None
        track_tuple = self.db.execute("SELECT * FROM " + "track " + "WHERE " + "location = " + location)
        t = track_tuple.fetchone()
        track = {}
        for i in range(0, 19):
            track[self._t_nfo[i]] = t[i]

        genres = self.db.execute("SELECT * FROM " + "genres " + "WHERE " + "location = " + location)
        g = []
        if genres is None:
            track["genres"] = None
        else:
            for genre in genres:
                g += [genre[1]]
            track["genres"] = g

        involved = self.db.execute("SELECT * FROM " + "genres " + "WHERE " + "location = " + location)
        i = []
        if involved is None:
            track["involved"] = None
        else:
            for involve in involved:  # TODO: Better naming
                i += [involve[1]]
            track["involved"] = i

        return track

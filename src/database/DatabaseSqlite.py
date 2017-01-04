from typing import List, Dict

import sqlite3

from src.database.IDatabaseAdapter import IDatabaseAdapter


class DatabaseSqlite(IDatabaseAdapter):
    def __init__(
            self,
            db_path: str):
        """
        :param db_path: Location where to Store DB
        """
        self.db = sqlite3.connect(db_path)  # type: sqlite3.Connection
        self.db.execute("CREATE TABLE IF NOT EXISTS track (title text, artist text, album text, \
                        location text primary key, imported bool, available bool, type text, init bool)")
        self.db.execute("CREATE TABLE IF NOT EXISTS involved(location text, feature text)")
        self.db.execute("CREATE TABLE IF NOT EXISTS genres(location text, genre text)")
        self._tag_information = ["location", "subtitle", "additional_artist1", "additional_artist2",
                                 "additional_artist3", "composer", "lyricist", "publisher", "year", "track_number",
                                 "bpm", "key", "mood", "length", "lyrics", "artist_url", "publisher_url", "file_type",
                                 "user_comment"]
        self.db.execute("CREATE TABLE IF NOT EXISTS trackTag(location text primary key, subtitle text, additional_artist1 text, \
                        additional_artist2 text, additional_artist3 text, composer text, lyricist text, \
                        publisher text, year text, track_number text, bpm text, key text, mood text, length text, \
                        lyrics text, artist_url text, publisher_url text, file_type text, user_comment text)")

    def __fetchAllTracks(self) -> List[tuple]:
        """
        Returns all stored Information from track
        :return: All stored Information from track in a List within Tuples
        """
        return self.db.execute("SELECT * FROM track").fetchall()

    def __getLocation(self, title: str, artist: str, album: str) -> str:
        """
        Returns location String
        :param title: title of location
        :param artist: artist of location
        :param album: album of location
        :return: Location as String for given information
        """
        return self.db.execute("SELECT location FROM track where title = ? AND artist = ? AND album = ?",
                               [title, artist, album]).fetchone()[0]

    def __addTag(self, tag_dict: dict, location: str) -> None:
        """
        :param tag_dict: Additional Track Metainformation
        :param location: Track Location
        :return: None
        """
        tag_informations = [location]
        for i in range(1, 19):
            if not tag_dict.get(self._tag_information[i]):  # TODO: Wrong membership test, use more readable style
                tag_informations.append(None)
            else:
                tag_informations.append(tag_dict.get(self._tag_information[i]))
        try:
            self.db.execute("INSERT INTO trackTag VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            tag_informations)
        except sqlite3.IntegrityError:
            self.db.execute("UPDATE trackTag SET subtitle = ?, additional_artist1 = ?, \
                        additional_artist2 = ?, additional_artist3 = ?, composer = ?, lyricist = ?, \
                        publisher = ?, year = ?, track_number = ?, bpm = ?, key = ?, mood = ?, length = ?, \
                        lyrics = ?, artist_url = ?, publisher_url = ?, file_type = ?, user_comment = ? WHERE \
                        location = ?)",
                            tag_informations[1:] + [tag_informations[0]])

        if tag_dict.get("genres") is None:
            self.db.execute("INSERT INTO genres VALUES(?, ?)",
                            [location, None])
        else:
            for gen in tag_dict["genres"]:
                try:
                    self.db.execute("INSERT INTO genres VALUES(?, ?)", [location, gen])
                except sqlite3.IntegrityError:
                    pass  # Here is nothing to do, cause in this case row already exist

        if tag_dict.get("involved") is None:
            self.db.execute("INSERT INTO involved VALUES(?, ?)", [location, None])
        else:
            for inv in tag_dict["involved"]:
                try:
                    self.db.execute("INSERT INTO involved VALUES(?, ?)", [location, inv])
                except sqlite3.IntegrityError:
                    pass  # Here is nothing to do, cause in this case row already exist

        self.db.commit()

    def addTrack(self, location: str,
                 title: str=None,
                 artist: str=None,
                 album: str=None,
                 format_type: str=None,
                 **kwargs) -> None:
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
        try:
            self.db.execute("INSERT INTO track VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [title, artist, album, location, False, False, format_type, False])
            # Will set Import True, Available False, initialized False   # FIXME: SQL-Inj. possible
        except sqlite3.IntegrityError:
            self.db.execute("UPDATE track SET title = ?, artist = ?, album = ?, imported = ?, available = ?, type = ?, \
            init = ? where location = ?", [title, artist, album, False, False, format_type, False, location])
            # Will set Import True, Available False, initialized False   # FIXME: SQL-Inj. possible
        self.db.commit()
        self.__addTag(kwargs, location)

    def setAllUninitialized(self) -> None:
        """
        sets all Data in Tracks marked as uninitialized
        :return: None
        """
        self.db.execute("UPDATE track set initialized = 0")
        self.db.commit()

    def setAllUnimported(self) -> None:
        """
        sets all Data in Tracks marked as unimported
        :return: None
        """
        self.db.execute("UPDATE track set imported = 0")
        self.db.commit()

    def setAllUnavailable(self) -> None:
        """
        sets all Data in Tracks marked as unavailable
        :return: None
        """
        self.db.execute("UPDATE track set available = 0")
        self.db.commit()

    def setTrackIsImported(self, title: str, artist: str, album: str) -> None:
        """
        Sets Tracks imported Attribute to True
        :param title: Title of Track
        :param artist: Artist of Track
        :param album: Album of Track
        :return: None
        """
        self.db.execute("UPDATE track SET imported = ? WHERE location = ?",
                        [True, self.__getLocation(title, artist, album)])
        self.db.commit()

    def setTrackIsInitialized(self, title: str, artist: str, album: str) -> None:
        """
        Sets Tracks init Attribute to True
        :param title: Title of Track
        :param artist: Artist of Track
        :param album: Album of Track
        :return: None
        """
        self.db.execute("UPDATE track SET init = ? WHERE location = ?",
                        [True, self.__getLocation(title, artist, album)])
        self.db.commit()

    def setTrackIsAvailable(self, title: str, artist: str, album: str) -> None:
        """
        Sets Tracks available Attribute to True
        :param title: Title of Track
        :param artist: Artist of Track
        :param album: Album of Track
        :return: None
        """
        self.db.execute("UPDATE track SET available = ? WHERE location = ?",
                        [True, self.__getLocation(title, artist, album)])
        self.db.commit()

    def getTracks(self) -> List[Dict[str, any]]:
        """
        Returns all Tracks in a List of Dictionary
        :return: List of Dictionary with information for Tracks stored in DB
        """
        result = []
        for track in self.db.execute("SELECT * FROM track").fetchall():
            result.append(
                {"title": track[0],
                 "artist": track[1],
                 "album": track[2],
                 "location": track[3],
                 "imported": track[4],
                 "available": track[5],
                 "type": track[6],
                 "initialized": track[7]}
            )  # Perhaps 4,5,7 convert to bool
        return result

    def getArtists(self) -> List[str]:
        """

        :return: All stored Artists in DB
        """
        artists = []
        artist_tuple = self.db.execute("SELECT artist FROM track GROUP BY artist").fetchall()
        for artist in artist_tuple:
            artists.append(artist[0])
        return artists

    def getAlbums(self) -> List[str]:
        """
        Returns all stored Albums
        :return: All stored Albums in DB
        """
        albums = []
        albums_tuple = self.db.execute("SELECT album FROM track GROUP BY album").fetchall()
        for album in albums_tuple:
            albums.append(album[0])
        return albums

    def getAlbumsByArtist(self, artist: str) -> List[str]:
        """
        Returns all stored Albums from given Artist
        :return: All stored Albums from given Artist
        """
        albums = []
        albums_tuple = self.db.execute("SELECT album FROM track WHERE artist = ? GROUP BY album", [artist]).fetchall()
        for album in albums_tuple:
            albums.append(album[0])
        return albums

    def getUnimported(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                where imported is 0
        """
        result = []
        for track in self.db.execute("SELECT * FROM track WHERE imported = ?", [False]):
            result.append(
                {"title": track[0],
                 "artist": track[1],
                 "album": track[2],
                 "location": track[3],
                 "imported": track[4],
                 "available": track[5],
                 "type": track[6],
                 "initialized": track[7]}
            )
        return result

    def getUnavailable(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    where available is 0
        """
        result = []
        for track in self.db.execute("SELECT * FROM track WHERE available = ?", [False]):
            result.append(
                {"title": track[0],
                 "artist": track[1],
                 "album": track[2],
                 "location": track[3],
                 "imported": track[4],
                 "available": track[5],
                 "type": track[6],
                 "initialized": track[7]}
            )
        return result

    def getTrack(self, title: str, artist: str, album: str) -> Dict[str, any]:
        """
        :param title: Title from Track to get
        :param artist: Artist from Track to get
        :param album: Album from Track to get
        :return: Dictionary with Keys: Title, Artist, Album, Location, imported, available and type
        """
        # FIXME: escape input strings
        track_tuple = self.db.execute("SELECT * FROM track WHERE title = ? AND artist = ? AND album = ? \
                                      AND imported = ? AND available = ? AND init = ?",
                                      [title, artist, album, True, True, True])
        track = track_tuple.fetchone()
        if track is None:
            return None
        track_dict = {"title": track[0],
                      "artist": track[1],
                      "album": track[2],
                      "location": track[3],
                      "imported": track[4],
                      "available": track[5],
                      "type": track[6],
                      "initialized": track[7]}
        return track_dict

    def getTracksByArtist(self, artist: str) -> List[Dict[str, any]]:
        """
        :param artist: Artist to get Tracks from
        :return: List of Dictionary based on given Artist
        """
        result = []
        for track in self.db.execute("SELECT * FROM track WHERE artist = ? AND imported = ? AND available = ? \
                                     AND init = ?", [artist, True, True, True]):
            result.append(
                {"title": track[0],
                 "artist": track[1],
                 "album": track[2],
                 "location": track[3],
                 "imported": track[4],
                 "available": track[5],
                 "type": track[6],
                 "initialized": track[7]}
            )
        return result

    def getTracksByAlbum(self, artist: str, album: str) -> List[Dict[str, any]]:
        """

        :param artist: Artist of Album to get Tracks from
        :param album: Album to get Tracks from
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    based on given Artist and Album
        """
        # FIXME: escape input strings
        result = []
        for track in self.db.execute("SELECT * FROM track WHERE artist = ? AND album = ? AND imported = ? AND \
                                     available = ? AND init = ?", [artist, album, True, True, True]):
            result.append(
                {"title": track[0],
                 "artist": track[1],
                 "album": track[2],
                 "location": track[3],
                 "imported": track[4],
                 "available": track[5],
                 "type": track[6],
                 "initialized": track[7]}
            )
        return result

    def getMetainformation(self, title: str, artist: str, album: str) -> Dict[str, any]:
        """
        :param title: Title to get Metainformation from
        :param artist: Artist to get Metainformation from
        :param album: Album to get Metainformation from
        :return: Dictionary with Metainformation based on given Artist, Title and Album
        """
        location = self.__getLocation(title, artist, album)
        if location is None:
            return None

        track_tuple = self.db.execute("SELECT * FROM trackTag WHERE location = ?", [location])
        t = track_tuple.fetchone()
        track = {}
        for i in range(0, 19):
            track[self._tag_information[i]] = t[i]

        genres = self.db.execute("SELECT genre FROM genres WHERE location = ?", [location]).fetchall()
        genre_of_track = []
        if not genres:
            track["genres"] = None
        else:
            for genre in genres:
                genre_of_track.append(genre[0])
            track["genres"] = genre_of_track

        involved = self.db.execute("SELECT feature FROM involved WHERE location = ?", [location]).fetchall()
        names = []
        if not involved:
            track["involved"] = None
        else:
            for feature in involved:
                names.append(feature[0])
            track["involved"] = names
        return track

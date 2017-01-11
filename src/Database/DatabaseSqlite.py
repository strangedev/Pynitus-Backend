"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Vivian Franz

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

from typing import List, Dict
import sqlite3

from src.Data.Tagging.TagSupport import TagValue, INTERNAL_NAMES, isListType
from src.Database.IDatabaseAdapter import IDatabaseAdapter


class DatabaseSqlite(IDatabaseAdapter):
    def __init__(
            self,
            db_path: str):
        """
        :param db_path: Location where to Store DB
        """
        # TODO: Map Type in Database
        self.db = sqlite3.connect(db_path)  # type: sqlite3.Connection
        table_start = "CREATE TABLE IF NOT EXISTS "
        track_start = table_start + "track (location text primary key, type text,"
        tag_start = table_start + "trackTag (location text primary key,"
        for x in INTERNAL_NAMES:
            if isListType(x):
                self.db.execute(table_start + x + " (location text primary key, " + x + " text)")
            elif x in ["title", "artist", "album", "type"]:
                track_start += x + " text, "
            elif x == "location":
                continue
            else:
                tag_start += x + " text, "
        tag_cmd = tag_start[:len(tag_start)-2] + ")"
        track_cmd = track_start + "imported bool, available bool, init bool)"
        self.db.execute(tag_cmd)
        self.db.execute(track_cmd)

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
        row = self.db.execute("SELECT location FROM track where title = ? AND artist = ? AND album = ?",
                              [title, artist, album]).fetchone()
        if not row:
            return None
        return row[0]

    def __addTag(self, track_tag: Dict[str, TagValue], location: str) -> None:
        """
        :param track_tag: Additional Track Metainformation
        :param location: Track Location
        :return: None
        """
        if not track_tag:
            return None
        sorted_tuple = []
        list_attribute = []
        for tag, value in track_tag.items():
            if isListType(tag):
                list_attribute.append(tag)
            else:
                if tag not in ["album", "artist", "title", "type"]:
                    sorted_tuple.append(tag)
        sorted_tuple = tuple(sorted_tuple)
        sorted_list = []
        question_mark = "?"
        update_str = "UPDATE trackTag SET {} = {}".format(sorted_tuple[0], track_tag[sorted_tuple[0]])
        for i in range(0, len(sorted_tuple)):
            sorted_list.append(track_tag[sorted_tuple[i]])
            if i > 0:
                question_mark += ", ?"
                update_str += ", {} = {}".format(sorted_tuple[i], track_tag[sorted_tuple[i]])
        update_str += " WHERE location = " + location

        for attribute in list_attribute:
            for tag in track_tag[attribute]:
                try:
                    self.db.execute("INSERT INTO {} (location, {}) VALUES(?,?)".format(attribute, attribute),
                                    [location, tag])
                except sqlite3.IntegrityError:
                    self.db.execute("UPDATE {} SET {} = {} WHERE location = ?".format(attribute, attribute, tag),
                                    [location])
        try:
            self.db.execute("INSERT INTO trackTag {} VALUES({})".format(sorted_tuple, question_mark),
                            sorted_list)
        except sqlite3.IntegrityError:
            self.db.execute(update_str)
        self.db.commit()

    def addTrack(self, location: str,
                 track_type: str,
                 track_tag: Dict[str, TagValue]) -> None:
        """
        :param location: Location of Track
        :param track_type: TrackType if its a Local File or for example a Youtube File
        :param track_tag: Track Metainformation
        :return: None
        """
        # FIXME: escape input strings
        try:
            self.db.execute("INSERT INTO track(title, artist, album, location, init, available, type, imported) \
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            [track_tag["title"], track_tag["artist"], track_tag["album"],
                             location, False, False, track_type, True])
            # Will set Import True, Available False, initialized False   # FIXME: SQL-Inj. possible
        except sqlite3.IntegrityError:
            self.db.execute("UPDATE track SET title = ?, artist = ?, album = ?, imported = ?, available = ?, type = ?, \
            init = ? where location = ?", [track_tag["title"], track_tag["artist"], track_tag["album"],
                                           False, False, track_type, False, location])
            # Will set Import True, Available False, initialized False   # FIXME: SQL-Inj. possible
        self.db.commit()
        self.__addTag(track_tag, location)

    def setAllUninitialized(self) -> None:
        """
        sets all Data in Tracks marked as uninitialized
        :return: None
        """
        self.db.execute("UPDATE track set init = 0")
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
        if not artist_tuple:
            return None
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
        if not albums_tuple:
            return None
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
        if not albums_tuple:
            return None
        for album in albums_tuple:
            albums.append(album[0])
        return albums

    def getUnimported(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                where imported is False
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
                    where available is False
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

    def getUninitialized(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    where init is False
        """
        result = []
        for track in self.db.execute("SELECT * FROM track WHERE init = ?", [False]):
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
        for tag in INTERNAL_NAMES:
            track[tag] = t[tag]

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

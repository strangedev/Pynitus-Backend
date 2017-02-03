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

from typing import List, Dict, Tuple
import sqlite3

from src.Data.Tagging.TagSupport import TagValue, INTERNAL_NAMES, isListType, TAGLIB_IDENTIFIER_LOOKUP
from src.Database.IDatabaseAdapter import IDatabaseAdapter


class DatabaseSqlite(IDatabaseAdapter):

    def __init__(
            self,
            db_path: str):
        """
        :param db_path: Location where to Store DB
        """
        # TODO: Map Type in Database
        self.db_path = db_path
        db = sqlite3.connect(db_path)
        table_start = "CREATE TABLE IF NOT EXISTS "
        track_start = table_start + "track (location text primary key, type text,"
        tag_start = table_start + "trackTag (location text primary key,"
        for x in INTERNAL_NAMES:
            if isListType(x):
                db.execute(table_start + x + " (location text primary key, " + x + " text)")
            elif x in ["title", "artist", "album", "type"]:
                track_start += x + " text, "
            elif x == "location":
                continue
            else:
                tag_start += x + " text, "
        tag_cmd = tag_start[:len(tag_start)-2] + ")"
        track_cmd = track_start + "imported bool, available bool, init bool)"
        db.execute(tag_cmd)
        db.execute(track_cmd)
        db.commit()
        db.close()

    @staticmethod
    def getTrackRowAsDict(track: List[any]) -> Dict[str, any]:
        if len(track) != 8:
            return None
        return {"title": track[0], "artist": track[1], "album": track[2], "location": track[3], "imported": track[4],
                "available": track[5], "type": track[6], "initialized": track[7]}

    @staticmethod
    def getTrackRowsAsListOfDict(tracks: List[any]) -> List[Dict[str, any]]:
        result = []
        for track in tracks:
            result.append(DatabaseSqlite.getTrackRowAsDict(track))
        return result

    def __executesAndCommit(self, cmd: List[Tuple[str, any]]) -> None:
        db = sqlite3.connect(self.db_path)
        for c in cmd:
            db.execute(c[0], c[1])
        db.commit()
        db.close()

    def __getOne(self, cmd: str, conditions: List[any]) -> Tuple:
        return sqlite3.connect(self.db_path).execute(cmd, conditions).fetchone()

    def __getMany(self, cmd: str, conditions: List[any]):
        return sqlite3.connect(self.db_path).execute(cmd, conditions).fetchall()

    def __fetchAllTracks(self) -> List[tuple]:
        """
        Returns all stored Information from track
        :return: All stored Information from track in a List within Tuples
        """
        return self.__getMany("SELECT * FROM track", [])

    def __getLocation(self, title: str, artist: str, album: str) -> str:
        """
        Returns location String
        :param title: title of location
        :param artist: artist of location
        :param album: album of location
        :return: Location as String for given information
        """
        row = self.__getOne("SELECT location FROM track where title = ? AND artist = ? AND album = ?",
                            [title, artist, album])
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
        tag_begin = "INSERT OR REPLACE INTO trackTag (location"
        tag_end = "VALUES (?"
        tag_values = [location]
        cmd = []

        for key, value in track_tag.items():
            if isListType(key):
                for v in value:
                    cmd.extend([("INSERT OR REPLACE INTO {} (location, {}) VALUES(?,?)".format(key, key),
                                 [location, v])])
            elif key not in ["title", "type", "artist", "album"]:
                tag_begin += ", " + key
                tag_end += ", ?"
                tag_values.append(value)

        tag_str = tag_begin + ") " + tag_end + ")"
        cmd.extend([(tag_str, tag_values)])
        self.__executesAndCommit(cmd)

    def addTrack(self, location: str,
                 track_type: str,
                 track_tag: Dict[str, TagValue]) -> None:
        """
        :param location: Location of Track
        :param track_type: TrackType if its a Local File or for example a Youtube File
        :param track_tag: Track Metainformation
        :return: None
        """
        self.__executesAndCommit([(
                                "INSERT OR REPLACE INTO track(title, artist, album, location, init, available, \
                                type, imported) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                [track_tag["title"], track_tag["artist"], track_tag["album"], location, False,
                                 False, track_type, False]
                                )])
        self.__addTag(track_tag, location)

    def setAllUninitialized(self) -> None:
        """
        sets all Data in Tracks marked as uninitialized
        :return: None
        """
        self.__executesAndCommit([("UPDATE track set init = 0", [])])

    def setAllUnimported(self) -> None:
        """
        sets all Data in Tracks marked as unimported
        :return: None
        """
        self.__executesAndCommit([("UPDATE track set imported = 0", [])])

    def setAllUnavailable(self) -> None:
        """
        sets all Data in Tracks marked as unavailable
        :return: None
        """
        self.__executesAndCommit([("UPDATE track set available = 0", [])])

    def setTrackIsImported(self, location: str) -> None:
        """
        Sets Tracks imported Attribute to True
        :param location: The tracks location
        :return: None
        """
        self.__executesAndCommit([("UPDATE track SET imported = ? WHERE location = ?", [True, location])])

    def setTrackIsInitialized(self, location: str) -> None:
        """
        Sets Tracks init Attribute to True
        :param location The tracks location
        :return: None
        """
        self.__executesAndCommit([("UPDATE track SET init = ? WHERE location = ?", [True, location])])

    def setTrackIsAvailable(self, location: str) -> None:
        """
        Sets Tracks available Attribute to True
        :param location The tracks location
        :return: None
        """
        self.__executesAndCommit([("UPDATE track SET available = ? WHERE location = ?", [True, location])])

    def getByLocation(self, location: str):
        return self.getTrackRowAsDict(list(self.__getOne(
                "SELECT title, artist, album, location, imported, available, type, init FROM track WHERE location = ?",
                [location])))

    def getTracks(self) -> List[Dict[str, any]]:
        """
        Returns all Tracks in a List of Dictionary
        :return: List of Dictionary with information for Tracks stored in DB
        """
        result = []
        for track in self.__getMany("SELECT title, artist, album, location, imported, available, type, init FROM track \
                                    WHERE imported = ? ", [True]):
            result.append(self.getTrackRowAsDict(list(track)))  # Perhaps 4,5,7 convert to bool
        return result

    def getArtists(self) -> List[str]:
        """

        :return: All stored Artists in DB
        """
        artists = []
        for artist in self.__getMany("SELECT artist FROM track WHERE imported = ? GROUP BY artist", [True]):
            artists.append(artist[0])
        return artists

    def getAlbums(self) -> List[Tuple[str, str]]:
        """
        Returns all stored Albums
        :return: All stored Albums in DB
        """
        albums = []
        for album in self.__getMany("SELECT artist, album FROM track WHERE imported = ? GROUP BY album", [True]):
            albums.append((album[0], album[1]))
        return albums

    def getAlbumsByArtist(self, artist: str) -> List[str]:
        """
        Returns all stored Albums from given Artist
        :return: All stored Albums from given Artist
        """
        albums = []
        for album in self.__getMany("SELECT album FROM track WHERE imported = ? AND artist = ? GROUP BY album",
                                    [True, artist]):
            albums.append(album[0])
        return albums

    def getUnimported(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                where imported is False
        """
        result = []
        for track in self.__getMany("SELECT title, artist, album, location, imported, available, type, init FROM track \
                                    WHERE imported = ?", [False]):
            result.append(self.getTrackRowAsDict(list(track)))
        return result

    def getUnavailable(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    where available is False
        """
        result = []
        for track in self.__getMany("SELECT title, artist, album, location, imported, available, type, init FROM \
                                         track WHERE available = ?", [False]):
            result.append(self.getTrackRowAsDict(list(track)))
        return result

    def getUninitialized(self) -> List[Dict[str, any]]:
        """
        :return: List of Dictionary with Keys: Title, Artits, Album, Location, imported, available and type
                    where init is False
        """
        result = []
        for track in self.__getMany("SELECT title, artist, album, location, imported, available, type, init \
                                    FROM track WHERE init = ?", [False]):
            result.append(self.getTrackRowAsDict(list(track)))
        return result

    def getTrack(self, location: str) -> Dict[str, any]:
        """
        :param location: The tracks location
        :return: Dictionary with Keys: Title, Artist, Album, Location, imported, available and type
        """
        # FIXME: escape input strings
        track = self.__getOne(
            "SELECT title, artist, album, location, imported, available, type, init \
            FROM track WHERE location = ? AND imported = ? AND available = ? AND init = ?",
            [location, 1, 1, 1]
        )
        if track is None:
            return None
        track_dict = self.getTrackRowAsDict(list(track))
        return track_dict

    def getTracksByArtist(self, artist: str) -> List[Dict[str, any]]:
        """
        :param artist: Artist to get Tracks from
        :return: List of Dictionary based on given Artist
        """
        result = []
        for track in self.__getMany("SELECT title, artist, album, location, imported, available, type, init FROM track \
                                    WHERE artist = ? AND imported = ? AND available = ?  AND init = ?",
                                    [artist, True, True, True]):
            result.append(self.getTrackRowAsDict(list(track)))
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
        for track in self.__getMany("SELECT title, artist, album, location, imported, available, type, init FROM track \
                                    WHERE artist = ? AND album = ? AND imported = ? AND available = ? AND init = ?",
                                    [artist, album, True, True, True]):
            result.append(self.getTrackRowAsDict(list(track)))
        return result

    def getMetainformation(self, location: str) -> Dict[str, any]:
        """
        :param location Location of track to get Metainformation from
        :return: Dictionary with Metainformation based on given location
        """
        if location is None:
            return None

        track = {"location": location}
        for tag in TAGLIB_IDENTIFIER_LOOKUP:
            if (tag not in ["artist", "location", "title", "album"]) and (not isListType(tag)):
                track[tag] = self.__getOne("SELECT {} FROM trackTag WHERE location = ?".format(tag), [location])[0]
            # TODO: Think of a better way...

        genres = self.__getMany("SELECT genres FROM genres WHERE location = ?", [location])
        genre_of_track = []
        if not genres:
            track["genres"] = None
        else:
            for genre in genres:
                genre_of_track.append(genre[0])
            track["genres"] = genre_of_track

        involved = self.__getMany("SELECT features FROM features WHERE location = ?", [location])
        names = []
        if not involved:
            track["features"] = None
        else:
            for feature in involved:
                names.append(feature[0])
            track["features"] = names
        return track

    def updateTrack(self, location: str, tag_info: Dict[str, TagValue]) -> None:
        self.__addTag(tag_info, location)
        self.__executesAndCommit([(
                                    "UPDATE track set title = ?,  artist = ?, album = ? WHERE location = ?",
                                    [tag_info["title"], tag_info["artist"], tag_info["album"], location]
                                )])

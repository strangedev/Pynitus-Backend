import os
import random
from unittest import TestCase

import sqlite3

from src.Data.Tagging.TagSupport import isListType, TAGLIB_IDENTIFIER_LOOKUP
from src.Database.DatabaseSqlite import DatabaseSqlite


class TestDatabaseSqlite(TestCase):
    def setUp(self):
        self.cur_path = os.getcwd() + "/testDatabasePynitus.db"
        self.test_size = 200
        self.imported_numbers = []
        self.available_numbers = []
        self.init_numbers = []
        self.all_true_numbers = []
        self.number_of_true_rows = 10
        for i in range(0, self.number_of_true_rows):
            if i == 0:
                self.all_true_numbers.append((random.randint(0, self.test_size)))
                self.imported_numbers.append(self.all_true_numbers[0])
                self.available_numbers.append(self.all_true_numbers[0])
                self.init_numbers.append(self.all_true_numbers[0])
                continue
            self.imported_numbers.append(random.randint(0, self.test_size))
            self.available_numbers.append(random.randint(0, self.test_size))
            self.init_numbers.append(random.randint(0, self.test_size))

        self.imported_numbers = sorted(set(self.imported_numbers), key=self.imported_numbers.index)
        self.available_numbers = sorted(set(self.available_numbers), key=self.available_numbers.index)
        self.init_numbers = sorted(set(self.init_numbers), key=self.init_numbers.index)

        db = sqlite3.connect(self.cur_path)
        self.test_db = DatabaseSqlite(self.cur_path)

        meta_string1 = "INSERT OR REPLACE INTO trackTag (location"
        meta_string2 = " VALUES(?"
        meta_data = ["{}"]
        meta_data_lists = {}
        for name, value in TAGLIB_IDENTIFIER_LOOKUP.items():
            if name in ["location", "artist", "title", "album", "type", "available", "imported", "init"]:
                continue
            if isListType(name):
                meta_name = name + " {}"
                meta_data_lists[meta_name] = "INSERT OR REPLACE INTO {} (location, {}) VALUES(?, ?)".format(name, name)
                continue
            meta_string1 += ", "
            meta_string1 += name
            meta_string2 += ", ?"
            meta_data.append(name + " {}")
        meta_string = meta_string1 + ")" + meta_string2 + ")"

        for i in range(0, self.test_size + 1):
            db.execute(
                "INSERT OR REPLACE INTO track ({}, {}, {}, {}, {}, {}, {}, {}) VALUES(?,?,?,?,?,?,?,?)".format(
                                                                                                            "location",
                                                                                                            "title",
                                                                                                            "artist",
                                                                                                            "album",
                                                                                                            "type",
                                                                                                            "imported",
                                                                                                            "available",
                                                                                                            "init"),
                [str(i), "title {}".format(str(i)), "artist {}".format(str(i)), "album {}".format(str(i)),
                 "type {}".format(str(i)), False, False, False])
            numbered_name_list = []
            for meta_data_name in meta_data:
                numbered_name_list.append(meta_data_name.format(str(i)))
            db.execute(meta_string, numbered_name_list)

            for key, value in meta_data_lists.items():
                db.execute(value, [str(i), key.format(str(i))])

            if i in self.imported_numbers:
                db.execute("UPDATE track set imported = 1 Where location = {}".format(i))
            if i in self.available_numbers:
                db.execute("UPDATE track set available = 1 Where location = {}".format(i))
            if i in self.init_numbers:
                db.execute("UPDATE track set init = 1 Where location = {}".format(i))
            if i in self.all_true_numbers:
                db.execute("UPDATE track set imported = 1, available = 1, init = 1 WHERE location = ?", [str(i)])

        db.commit()

    def doCleanups(self):
        os.remove(self.cur_path)

    def test_addTrack(self):
        tag_lookup = TAGLIB_IDENTIFIER_LOOKUP
        tag_lookup["features"] = ["FEATURES"]
        tag_lookup["genres"] = ["GENRE"]
        tag_lookup["location"] = "test"
        self.test_db.addTrack("test", "test_type", tag_lookup)
        db = sqlite3.connect(self.cur_path)
        db.close()
        db = sqlite3.connect(self.cur_path)
        t = db.execute(
            "SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM track WHERE location = ?".format("location", "title",
                                                                                         "artist", "album", "type",
                                                                                         "imported", "available",
                                                                                         "init"), ["test"]).fetchone()
        track_dict = {}

        z = 0
        for n in ["location", "title", "artist", "album"]:
            track_dict[n] = t[z]
            z += 1

        for key in TAGLIB_IDENTIFIER_LOOKUP.keys():
            if key in ["location", "title", "artist", "album", "type", "imported", "available", "init"]:
                continue
            if isListType(key):
                key_list = []
                for i in db.execute("SELECT {} from {} WHERE location = ?".format(key, key), ["test"]).fetchall():
                    key_list.append(i[0])
                track_dict[key] = key_list
                continue
            track_dict[key] = db.execute("SELECT {} from trackTag WHERE location = ?".format(key),
                                         ["test"]).fetchone()[0]
        self.assertDictEqual(track_dict, tag_lookup)

    def test_getTrackRowAsDict(self):
        self.assertDictEqual(self.test_db.getTrackRowAsDict(
                            ["title", "artist", "album", "location", "imported", "available", "type", "initialized"]),
                            {"title": "title", "artist": "artist", "album": "album", "location": "location",
                             "initialized": "initialized"}
        )

    def test_getTrackRowsAsListOfDict(self):
        list_inp = []
        eq_dict = []
        for i in range(0, 10):
            l = []
            e = {}
            for j in ["title", "artist", "album", "location", "imported", "available", "type", "initialized"]:
                k = (j + " {}").format(str(i))
                l.append(k)
                e[j] = k
            list_inp.append(l)
            eq_dict.append(e)
        self.assertListEqual(self.test_db.getTrackRowsAsListOfDict(list_inp), eq_dict)

    def test_setAllUninitialized(self):
        self.assertEqual(
            len(sqlite3.connect(self.cur_path).execute("SELECT * from track WHERE init = ?", [True]).fetchall()),
            len(self.init_numbers))
        self.test_db.setAllUninitialized()
        self.assertListEqual(
            sqlite3.connect(self.cur_path).execute("SELECT * from track WHERE init = ?", [True]).fetchall(), []
        )

    def test_setAllUnimported(self):
        self.assertEqual(
            len(sqlite3.connect(self.cur_path).execute("SELECT * from track WHERE imported = ?", [True]).fetchall()),
            len(self.imported_numbers))
        self.test_db.setAllUnimported()
        self.assertListEqual(
            sqlite3.connect(self.cur_path).execute("SELECT * from track WHERE imported = ?", [True]).fetchall(), []
        )

    def test_setAllUnavailable(self):
        self.assertEqual(
            len(sqlite3.connect(self.cur_path).execute("SELECT * from track WHERE available = ?", [True]).fetchall()),
            len(self.available_numbers))
        self.test_db.setAllUnavailable()
        self.assertListEqual(
            sqlite3.connect(self.cur_path).execute("SELECT * from track WHERE available = ?", [True]).fetchall(), []
        )

    def test_setTrackIsImported(self):
        location_track = sqlite3.connect(self.cur_path).execute(
                                    "SELECT location, imported from track WHERE imported = ?", [False]).fetchone()
        self.assertIsNotNone(location_track[0])
        self.assertFalse(location_track[1])
        self.test_db.setTrackIsImported(location_track[0])
        self.assertTrue(sqlite3.connect(self.cur_path).execute(
            "SELECT imported from track WHERE location = ?", [location_track[0]]).fetchone()[0])

    def test_setTrackIsInitialized(self):
        location_track = sqlite3.connect(self.cur_path).execute(
                                    "SELECT location, init from track WHERE init = ?", [False]).fetchone()
        self.assertIsNotNone(location_track[0])
        self.assertFalse(location_track[1])
        self.test_db.setTrackIsInitialized(location_track[0])
        self.assertTrue(sqlite3.connect(self.cur_path).execute(
            "SELECT init from track WHERE location = ?", [location_track[0]]).fetchone()[0])

    def test_setTrackIsAvailable(self):
        location_track = sqlite3.connect(self.cur_path).execute(
                                    "SELECT location, available from track WHERE available = ?", [False]).fetchone()
        self.assertIsNotNone(location_track[0])
        self.assertFalse(location_track[1])
        self.test_db.setTrackIsAvailable(location_track[0])
        self.assertTrue(sqlite3.connect(self.cur_path).execute(
            "SELECT available from track WHERE location = ?", [location_track[0]]).fetchone()[0])

    def test_getByLocation(self):
        test_dict = {"location": "22", "artist": "artist 22", "title": "title 22", "album": "album 22",
                     "imported": 0, "available": 0, "type": "type 22", "initialized": 0}

        if 22 in self.imported_numbers:
            test_dict["imported"] = 1
        if 22 in self.available_numbers:
            test_dict["available"] = 1
        if 22 in self.init_numbers:
            test_dict["initialized"] = 1

        self.assertDictEqual(self.test_db.getByLocation("22"), test_dict)

    def test_getTracks(self):
        self.assertEqual(len(self.test_db.getTracks()), len(self.imported_numbers))

    def test_getArtists(self):
        imp = []
        for i in self.imported_numbers:
            imp.append("artist {}".format(i))
        self.assertListEqual(sorted(self.test_db.getArtists()), sorted(imp))

    def test_getAlbums(self):
        imp = []
        for i in self.imported_numbers:
            imp.append(("artist {}".format(i), "album {}".format(i)))
        self.assertEqual(len(self.test_db.getAlbums()), len(imp))
        for artist_album in self.test_db.getAlbums():
            self.assertTrue(artist_album in imp)

    def test_getAlbumsByArtist(self):
        imp1 = ["album {}".format(self.imported_numbers[0])]
        imp2 = ["album {}".format(self.imported_numbers[1])]
        self.assertEqual(self.test_db.getAlbumsByArtist("artist {}".format(self.imported_numbers[0])), imp1)
        self.assertEqual(self.test_db.getAlbumsByArtist("artist {}".format(self.imported_numbers[1])), imp2)

    def test_getUnimported(self):
        self.assertTrue(len(self.test_db.getUnimported()), (self.test_size - (len(self.imported_numbers))))

    def test_getUnavailable(self):
        self.assertTrue(len(self.test_db.getUnavailable()), (self.test_size - (len(self.available_numbers))))

    def test_getUninitialized(self):
        self.assertTrue(len(self.test_db.getUninitialized()), (self.test_size - (len(self.init_numbers))))

    def test_getTrack(self):
        number = self.all_true_numbers[0]
        test_dict = {"location": "{}".format(number), "artist": "artist {}".format(number),
                     "title": "title {}".format(number), "album": "album {}".format(number), "imported": 1,
                     "available": 1, "type": "type {}".format(number), "initialized": 1}
        self.assertDictEqual(self.test_db.getTrack(str(number)), test_dict)

    def test_getTracksByArtist(self):
        number = self.all_true_numbers[0]
        test_dict = {"location": "{}".format(number), "artist": "artist {}".format(number),
                     "title": "title {}".format(number), "album": "album {}".format(number), "imported": 1,
                     "available": 1, "type": "type {}".format(number), "initialized": 1}
        self.assertDictEqual(self.test_db.getTracksByArtist("artist {}".format(number))[0], test_dict)

    def test_getTracksByAlbum(self):
        number = self.all_true_numbers[0]
        test_dict = {"location": "{}".format(number), "artist": "artist {}".format(number),
                     "title": "title {}".format(number), "album": "album {}".format(number), "imported": 1,
                     "available": 1, "type": "type {}".format(number), "initialized": 1}
        self.assertDictEqual(self.test_db.getTracksByAlbum("artist {}".format(number), "album {}".format(number))[0],
                             test_dict)

    def test_getMetainformation(self):
        number = 63
        test_dict = {"location": str(number)}
        for i in TAGLIB_IDENTIFIER_LOOKUP.keys():
            if i in ["artist", "title", "album", "location"]:
                continue
            if isListType(i):
                test_dict[i] = [(i + " {}").format(number)]
                continue
            test_dict[i] = (i + " {}").format(number)

        for key, value in self.test_db.getMetainformation(str(number)).items():
            if isListType(key):
                self.assertListEqual(value, test_dict[key])
                continue
            self.assertEqual(value, test_dict[key])

    def test_updateTrack(self):
        self.assertListEqual(
            list(sqlite3.connect(self.cur_path).execute(
                "SELECT title, artist, album from track WHERE location = ?",
                ["1"]).fetchone()),
            ["title 1", "artist 1", "album 1"]
            )
        self.test_db.updateTrack("1", {"title": "other_title", "artist": "other_artist", "album": "other_album"})
        self.assertListEqual(list(sqlite3.connect(self.cur_path).execute("SELECT title, artist, album from track \
                                                                        WHERE location = ?", ["1"]).fetchone()),
                             ["other_title", "other_artist", "other_album"])

import requests
import unittest

from Pynitus.api.request_util import Response


class TestTracks(unittest.TestCase):

    track_count = 1000 - 5
    pagination_offset = 111
    pagination_offset = 222

    """
    Unavailable Tracks: 1, 32, 33
    Unimported Tracks: 30, 31
    """

    def setUp(self): pass

    # tracks.all

    def test_tracks_all(self):
        response = requests.get("http://127.0.0.1:5000/tracks/all").json()
        self.assertEqual(len(response), self.track_count)

    def test_tracks_all_pagination_offset(self):  # TODO

        payload = {"offset": self.pagination_offset}
        response = requests.get("http://127.0.0.1:5000/tracks/all", params=payload).json()

        self.assertEqual(len(response), self.track_count - self.pagination_offset)

    def test_tracks_all_pagination_amount(self):

        payload = {"amount": self.pagination_offset}
        response = requests.get("http://127.0.0.1:5000/tracks/all", params=payload).json()

        self.assertLessEqual(len(response), self.pagination_offset)

    def test_tracks_all_invalid_param_offset(self):

        payload = {"offset": "invalid"}
        response = requests.get("http://127.0.0.1:5000/tracks/all", params=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.BAD_REQUEST)

    def test_tracks_all_invalid_param_amount(self):

        payload = {"amount": "invalid"}
        response = requests.get("http://127.0.0.1:5000/tracks/all", params=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.BAD_REQUEST)

    # tracks.unavailable

    def test_tracks_unavailable(self):
        response = requests.get("http://127.0.0.1:5000/tracks/unavailable").json()
        self.assertEqual(len(response), 3)

    def test_tracks_unavailable_pagination_offset(self):

        payload = {"offset": 1}
        response = requests.get("http://127.0.0.1:5000/tracks/unavailable", params=payload).json()

        for item in response:
            self.assertGreaterEqual(item["id"], 32)

    def test_tracks_unavailable_pagination_amount(self):

        payload = {"amount": 1}
        response = requests.get("http://127.0.0.1:5000/tracks/unavailable", params=payload).json()

        for item in response:
            self.assertEqual(item["id"], 1)

    def test_tracks_unavailable_invalid_param_offset(self):

        payload = {"offset": "invalid"}
        response = requests.get("http://127.0.0.1:5000/tracks/unavailable", params=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.BAD_REQUEST)

    def test_tracks_unavailable_invalid_param_amount(self):

        payload = {"amount": "invalid"}
        response = requests.get("http://127.0.0.1:5000/tracks/unavailable", params=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.BAD_REQUEST)

    # tracks.unimported

    def test_tracks_unimported(self):
        response = requests.get("http://127.0.0.1:5000/tracks/unimported").json()
        self.assertEqual(len(response), 2)

    def test_tracks_unimported_pagination_offset(self):

        payload = {"offset": 1}
        response = requests.get("http://127.0.0.1:5000/tracks/unimported", params=payload).json()

        for item in response:
            self.assertEqual(item["id"], 31)

    def test_tracks_unimported_pagination_amount(self):

        payload = {"amount": 1}
        response = requests.get("http://127.0.0.1:5000/tracks/unimported", params=payload).json()

        for item in response:
            self.assertEqual(item["id"], 30)

    def test_tracks_unimported_invalid_param_offset(self):

        payload = {"offset": "invalid"}
        response = requests.get("http://127.0.0.1:5000/tracks/unimported", params=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.BAD_REQUEST)

    def test_tracks_unimported_invalid_param_amount(self):

        payload = {"amount": "invalid"}
        response = requests.get("http://127.0.0.1:5000/tracks/unimported", params=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.BAD_REQUEST)

    # other...

    def test_tracks_artist(self):

        for i in range(471, 474):

            request_url = "http://127.0.0.1:5000/tracks/artist/{}".format(i)
            response = requests.get(request_url).json()

            for track in response:
                self.assertEqual(track["id"], i)

    def test_tracks_album(self):

        for i in range(471, 474):

            request_url = "http://127.0.0.1:5000/tracks/album/{}".format(i)
            response = requests.get(request_url).json()

            for track in response:
                self.assertEqual(track["id"], i)

    def test_tracks_id(self):

        for i in range(471, 474):

            request_url = "http://127.0.0.1:5000/tracks/id/{}".format(i)
            response = requests.get(request_url).json()

            self.assertEqual(response["id"], i)

if __name__ == '__main__':
    unittest.main()
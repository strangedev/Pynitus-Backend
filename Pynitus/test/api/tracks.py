import requests
import unittest


class TestTracks(unittest.TestCase):

    track_count = 1000
    pagination_start = 111
    pagination_limit = 222


    def setUp(self):
        pass


    def test_tracks_all(self):
        response = requests.get("http://127.0.0.1:5000/tracks/all").json()
        self.assertEqual(len(response), self.track_count)

    def test_tracks_all_pagination_start(self):

        payload = {"start": self.pagination_start}
        response = requests.get("http://127.0.0.1:5000/tracks/all", params=payload).json()

        for api_object in response:
            self.assertGreaterEqual(api_object["id"], self.pagination_start)

    def test_tracks_all_pagination_limit(self):

        payload = {"amount": self.pagination_limit}
        response = requests.get("http://127.0.0.1:5000/tracks/all", params=payload).json()

        self.assertLessEqual(len(response), self.pagination_limit)

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
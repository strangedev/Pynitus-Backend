import requests
import unittest


class TestAlbums(unittest.TestCase):

    album_count = 1000
    pagination_start = 111
    pagination_limit = 222


    def setUp(self):
        pass


    def test_albums_all(self):
        response = requests.get("http://127.0.0.1:5000/albums/all").json()
        self.assertEqual(len(response), self.album_count)

    def test_albums_all_pagination_start(self):

        payload = {"start": self.pagination_start}
        response = requests.get("http://127.0.0.1:5000/albums/all", params=payload).json()

        for api_object in response:
            self.assertGreaterEqual(api_object["id"], self.pagination_start)

    def test_albums_all_pagination_limit(self):

        payload = {"amount": self.pagination_limit}
        response = requests.get("http://127.0.0.1:5000/albums/all", params=payload).json()

        self.assertLessEqual(len(response), self.pagination_limit)

    def test_albums_artist(self):

        for i in range(471, 474):

            request_url = "http://127.0.0.1:5000/albums/artist/{}".format(i)
            response = requests.get(request_url).json()

            for album in response:
                self.assertEqual(album["id"], i)

    def test_albums_id(self):

        for i in range(471, 474):

            request_url = "http://127.0.0.1:5000/albums/id/{}".format(i)
            response = requests.get(request_url).json()

            self.assertEqual(response["id"], i)

if __name__ == '__main__':
    unittest.main()
import requests
import unittest

from tinnitus import remote

from Pynitus.api.request_util import Response


class TestQueue(unittest.TestCase):

    sample_track_ids = [
        42,
        137,
        299,
        698,
    ]


    def setUp(self):
        pass

    def test_queue_current_empty(self):
        response = requests.get("http://127.0.0.1:5000/queue/current").json()
        self.assertEqual(response, None)

    def test_queue_items_empty(self):
        response = requests.get("http://127.0.0.1:5000/queue/items").json()
        self.assertListEqual(response, [])

    def test_queue_add_one(self):

        payload = {"track_id": "14"}
        response = requests.post("http://127.0.0.1:5000/queue/add", data=payload).json()

        self.assertEqual(response["success"], True)

        with remote() as r:
            r.clear()

    def test_queue_add_one_invalid_id(self):

        payload = {"track_id": 1001}
        response = requests.post("http://127.0.0.1:5000/queue/add", data=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.INVALID_OBJECT_ID)

    def test_queue_add_one_unavailable(self):

        payload = {"track_id": str(self.sample_track_ids[0])}
        response = requests.post("http://127.0.0.1:5000/queue/add", data=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.TRACK_UNAVAILABLE)

    def test_queue_remove_one(self):

        payload = {"track_id": "14"}
        response = requests.post("http://127.0.0.1:5000/queue/add", data=payload).json()

        self.assertEqual(response["success"], True)

        payload = {"track_id": "14"}
        response = requests.post("http://127.0.0.1:5000/queue/remove", data=payload).json()

        self.assertEqual(response["success"], True)

        with remote() as r:
            r.clear()

    def test_queue_remove_not_in_queue(self):

        payload = {"track_id": "10"}
        response = requests.post("http://127.0.0.1:5000/queue/remove", data=payload).json()

        self.assertEqual(response["success"], False)
        self.assertEqual(response["reason"], Response.NOT_IN_QUEUE)

        with remote() as r:
            r.clear()



if __name__ == '__main__':
    unittest.main()

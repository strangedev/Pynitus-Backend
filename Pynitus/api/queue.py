from flask import request

from Pynitus import app
from Pynitus.api.encoders import TrackEncoder
from Pynitus.model import artists
from Pynitus.model import tracks
from Pynitus.player import queue


@app.route('/queue/items', methods=['GET'])
def queue_all():
    return TrackEncoder().encode([tracks.get(i) for i in queue.queue()])


@app.route('/queue/current', methods=['GET'])
def queue_current():
    return TrackEncoder().encode(tracks.get(queue.current()))

from flask import g
from flask import json

from Pynitus import app
from Pynitus.api.encoders import TrackEncoder
from Pynitus.api.request_util import Response

from Pynitus.api.request_util import expect
from Pynitus.model import tracks
from Pynitus.model.db.database import persistance
from Pynitus.player import player
from Pynitus.player import queue


@app.route('/queue/items', methods=['GET'])
def queue_items():
    tracks_in_queue = [tracks.get(i) for i in queue.queue()]
    return TrackEncoder().encode(tracks_in_queue)


@app.route('/queue/current', methods=['GET'])
def queue_current():
    return TrackEncoder().encode(tracks.get(queue.current()))


@app.route('/queue/add', methods=['POST'])
@expect([('track_id', int)])
def queue_add(track_id=None):

    track = tracks.get(track_id)

    if track is None:
        return json.dumps({
            'success': False,
            'reason': Response.INVALID_OBJECT_ID
        })

    if not track.status.imported:
        return json.dumps({
            'success': False,
            'reason': Response.TRACK_UNAVAILABLE
        })

    with persistance():
        track.status.available = player.available(track.mrl, track.backend)

    if not track.status.available:
        return json.dumps({
            'success': False,
            'reason': Response.TRACK_UNAVAILABLE
        })

    queue.add(track_id, g._user_token)

    return json.dumps({
        'success': True
    })

@app.route('/queue/remove', methods=['POST'])
@expect([('track_id', int)])
def queue_remove(track_id=None):

    if track_id not in queue.queue():
        return json.dumps({
            'success': False,
            'reason': Response.NOT_IN_QUEUE
        })

    queue.remove(track_id)

    return json.dumps({
        'success': True
    })
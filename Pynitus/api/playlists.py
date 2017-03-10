from flask import g
from flask import json

from Pynitus import app
from Pynitus.api.encoders import PlaylistEncoder
from Pynitus.api.request_util import expect_optional, expect, Response
from Pynitus.auth import user_cache
from Pynitus.model import playlists


@app.route('/playlists/all', methods=['GET'])
@expect_optional([('offset', int), ('amount', int)])
def playlists_all(offset=0, amount=0):
    return PlaylistEncoder().encode(playlists.all(offset=offset, limit=amount))


@app.route('/playlists/id/<int:playlist_id>', methods=['GET'])
def playlists_get(playlist_id):
    return PlaylistEncoder().encode(playlists.get(playlist_id))


@app.route('/playlists/user/<str:username>', methods=['GET'])
def playlists_user(username):
    return PlaylistEncoder().encode(playlists.from_user(username))


@app.route('/playlists/create', methods=['PUT'])
@expect([('name', str)])
def playlists_create(name=None):
    if not user_cache.exists(g.user_token):
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    return json.dumps({
        'success': True,
        'result': PlaylistEncoder().default(playlists.create(user_cache.whois(g.user_token), name))
    })


@app.route('/playlists/add', methods=['PUT'])
@expect([('track_id', int), ('playlist_id', int)])
def playlists_add(track_id=0, playlist_id=0):
    # TODO: Make more beautiful
    if not user_cache.exists(g.user_token):
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    if user_cache.whois(g.user_token) != playlists.get(playlist_id).username:
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    return json.dumps({
        'success': playlists.add_track(playlist_id, track_id)
    })


@app.route('/playlists/remove_track', methods=['DELETE'])
@expect([('track_id', int), ('playlist_id', int)])
def playlists_remove_track(track_id=0, playlist_id=0):
    # TODO: Make more beautiful
    if not user_cache.exists(g.user_token):
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    if user_cache.whois(g.user_token) != playlists.get(playlist_id).username:
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    return json.dumps({
        'success': playlists.remove_track(playlist_id, track_id)
    })


@app.route('/playlists/remove', methods=['DELETE'])
@expect([('playlist_id', int)])
def playlists_remove(playlist_id=0):
    # TODO: Make more beautiful
    if not user_cache.exists(g.user_token):
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    if user_cache.whois(g.user_token) != playlists.get(playlist_id).username:
        return json.dumps({
            'success': False,
            'reason': Response.UNAUTHORIZED
        })

    return json.dumps({
        'success': playlists.remove(playlist_id)
    })

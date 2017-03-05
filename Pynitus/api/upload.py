from flask import json
from flask import request
from werkzeug.utils import secure_filename

from Pynitus import app
from Pynitus import upload
from Pynitus.api.encoders import DetailedTrackEncoder
from Pynitus.api.request_util import Response
from Pynitus.io.storage import get_storage_path
from Pynitus.model.db.models import Track


@app.route('/upload/plugins', methods=['GET'])
def upload_plugins():
    known_plugins = upload.get_plugins()

    for name in known_plugins.keys():
        known_plugins[name] = {k: v for k, v in known_plugins[name].items() if k != "path"}
    return json.dumps(known_plugins)


@app.route('/upload/<plugin_name>', methods=['PUT'])
def upload_do(plugin_name: str):

    arguments = dict({})
    required_arguments = upload.get_plugin_description(plugin_name)["arguments"]

    for name, attributes in required_arguments.items():

        if attributes["type"] == "file":

            if 'file' not in request.files:
                return json.dumps({
                    "success": False,
                    "reason": Response.BAD_REQUEST
                })

            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                return json.dumps({
                    "success": False,
                    "reason": Response.BAD_REQUEST
                })

            filename = secure_filename(file.filename)
            storage_path = get_storage_path(filename)
            file.save(storage_path)

            arguments[name] = storage_path

        else:

            value = request.args.get(name)
            if value is None:
                return json.dumps({
                    "success": False,
                    "reason": Response.BAD_REQUEST
                })

            arguments[name] = value

    track = upload.track_from_upload(plugin_name, **arguments)
    if not isinstance(track, Track):
        return json.dumps({
            "success": False,
            "reason": track
        })

    return json.dumps({
        "success": True,
        "result": DetailedTrackEncoder().default(track)
    })

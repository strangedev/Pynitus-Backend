import importlib.util
import os
from typing import Optional, Dict, Any

from Pynitus.api.request_util import Response
from Pynitus.framework import memcache
from Pynitus.model import tracks
from Pynitus.model.db.database import persistance, db_session
from Pynitus.model.db.models import Track


class TrackRecord(object):

    def __init__(self):
        self.artist = None
        self.album = None
        self.title = None
        self.backend = None
        self.mrl = None

        # TODO: tag info


def __load_plugin(name, plugin_path):
    spec = importlib.util.spec_from_file_location(name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def __is_plugin(module):

    attributes_exist = all([
            hasattr(module, "name"),
            hasattr(module, "description"),
            hasattr(module, "arguments"),
            hasattr(module, "handle")
        ])

    if not attributes_exist:
        return False

    attributes_well_formed = all([
            type(module.name) == str,
            type(module.description) == str,
            type(module.arguments) == dict,
            len(module.arguments) > 0,
            #all([arg.get("name") is not None for arg in module.arguments]),
            callable(module.handle)
        ])

    return attributes_well_formed#


def __discover_plugins():

    plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    include_paths = [plugin_dir]
    plugins = dict({})

    with open(os.path.join(plugin_dir, 'include.txt')) as f:
        contents = f.read()

    if contents is not None:
        contents = contents.split("\n")
        include_paths.extend([path for path in contents if path != ""])

    for plugin_path in include_paths:
        try:

            for filename in os.listdir(plugin_path):

                absolute_path = os.path.join(plugin_path, filename)
                name, ext = os.path.splitext(filename)

                if ext != '.py': continue

                try:
                    module = __load_plugin(name, absolute_path)
                except: continue

                if __is_plugin(module):
                    plugins[module.__name__] = {
                            'display_name': module.name,
                            'path': absolute_path,
                            'description': module.description,
                            'arguments': module.arguments
                        }

        except: continue

    memcache.set("upload.plugins", plugins)


def init_upload():
    __discover_plugins()


def get_plugins():
    return memcache.get("upload.plugins")


def get_plugin_description(name: str) -> Dict[str, Any]:
    return memcache.get("upload.plugins").get(name)


def __cleanup(mrl):
    if os.path.exists(mrl):
        os.remove(mrl)


def track_from_upload(name, **kwargs) -> Optional[Track]:
    plugin_description = memcache.get("upload.plugins").get(name)

    if plugin_description is None:
        return Response.INVALID_PLUGIN

    plugin = __load_plugin(name, plugin_description["path"])
    track_record = plugin.handle(**kwargs)  # type: TrackRecord

    if track_record.backend is None or track_record.mrl is None:
        return Response.PLUGIN_ERROR

    if tracks.exists(
            track_record.title,
            track_record.artist,
            track_record.album
    ):
        __cleanup(track_record.mrl)
        return Response.TRACK_EXISTS

    track = None
    with persistance():

        track = tracks.get_or_create(
            track_record.title,
            track_record.artist,
            track_record.album
        )

        track.backend = track_record.backend
        track.mrl = track_record.mrl

        # TODO: tag info
        db_session.add(track)

    return track
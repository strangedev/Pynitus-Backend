import os
from pathlib import Path
import importlib.util

import Pynitus

PLUGIN_PATH = ""

backends = dict({})

importers = dict({})


def init_plugins():
    global plugins

    plugin_path = os.path.join(Path(os.path.join(*Path(Pynitus.__file__).parts[0:-2])).as_posix(), 'plugins')

    for dirname in os.listdir(plugin_path):
        absolute_path = os.path.join(plugin_path, dirname)

        if '__init__.py' not in os.listdir(absolute_path):
            continue

        spec = importlib.util.spec_from_file_location(dirname, os.path.join(absolute_path, '__init__.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        is_backend = False
        is_importer = False

        try:
            is_backend =all([
                hasattr(module, "init"), callable(getattr(module, "init")),
                hasattr(module, "play"), callable(getattr(module, "play")),
                hasattr(module, "pause"), callable(getattr(module, "pause")),
                hasattr(module, "stop"), callable(getattr(module, "stop"))])

        except Exception: pass

        try:
            is_importer = all([
                hasattr(module, "name"),
                hasattr(module, "description"),
                hasattr(module, "attributes"),
                hasattr(module, "backend"),
                hasattr(module, "transform") and callable(getattr(module, "transform"))
            ])

        except Exception: pass

        if is_backend:
            backends[dirname] = module

        if is_importer:
            importers[dirname] = module

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
            is_backend = hasattr(module, "init") and callable(getattr(module, "init"))
            is_backend = is_backend and hasattr(module, "play") and callable(getattr(module, "play"))
            is_backend = is_backend and hasattr(module, "pause") and callable(getattr(module, "pause"))
            is_backend = is_backend and hasattr(module, "stop") and callable(getattr(module, "stop"))

        except Exception as e:
            pass

        try:
            is_importer = hasattr(module, "name")
            is_importer = is_importer and hasattr(module, "description")
            is_importer = is_importer and hasattr(module, "attributes")
            is_importer = is_importer and hasattr(module, "backend")
            is_importer = is_importer and hasattr(module, "transform") and callable(getattr(module, "transform"))

        except Exception as e:
            pass

        if is_backend:
            backends[dirname] = module

        if is_importer:
            importers[dirname] = module

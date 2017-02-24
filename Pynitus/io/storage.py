import os

from werkzeug.utils import secure_filename

from Pynitus.io import config


def init_storage():
    upload_path = config.get("upload_path")

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

def get_storage_path(filename="") -> str:

    upload_path = config.get("upload_path")

    if filename == "": filename  = os.urandom(32).hex()
    filename = secure_filename(filename)

    storage_path = os.path.join(upload_path, filename)
    file_exists = os.path.exists(storage_path)

    attempt = 1
    while file_exists:
        filename = "{}_{}".format(filename, attempt)
        storage_path = os.path.join(upload_path, filename)
        file_exists = os.path.exists(storage_path)

    return storage_path

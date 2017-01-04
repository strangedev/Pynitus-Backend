import taglib


class ID3TagReader(object):
    def __init__(self, file_path: str) -> None:
        self.audio_file = taglib.File(file_path)
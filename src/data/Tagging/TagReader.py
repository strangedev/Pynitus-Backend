import taglib
from typing import Dict


class TagReader(object):
    def __init__(self, file_path: str) -> None:
        self.audio_file = taglib.File(file_path)

    def readTag(self) -> Dict[str, any]:
        pass

    def writeTag(self, key: str, **kwargs) -> None:
        """

        :param key: key to Change
        :param kwargs: value of Key
        :return: None
        """
        pass
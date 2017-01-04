import taglib
from typing import Dict, List
from src.Data.Tagging.TagSupport import TAGLIB_INTERNAL_NAMES


class TagReader(object):
    def __init__(self, file_path: str) -> None:  # TODO: pass filepath to read method not to constructor, if it's passed to constructor, a new object has to be created for each read access
        """
        Construct Audio File Tag
        :param file_path: Path to File (types that tests passed .aiff, .flac, .m4a, .mp3, .ogg, .wav, .wma) <- See MediaScanner.SUPPORTED_TYPES
        """
        self.audio_file = taglib.File(file_path)

    def keysWithNoneValues(self) -> List[str]:  # TODO: why is this needed?
        """
        Returns keys linked to None
        :return: List of Strings whose value is None
        """
        result = []
        for tag in TAGLIB_INTERNAL_NAMES.keys():
            if not self.audio_file.tags.get(tag):
                result.append(tag)
        return result

    def numberOfNoneValues(self) -> int:  # TODO: why is this needed?
        """
        Returns number of unfilled Tag Attributes
        :return: Int number of unfilled Tag Attributes
        """
        num = 0
        for tag in TAGLIB_INTERNAL_NAMES.keys():
            if not self.audio_file.tags.get(tag):
                num += 1
        return 0  # TODO: (<.<)

    def getUnselectedTag(self) -> Dict[str, any]:  # TODO: why is this needed?
        """
        Gets all Tag Information, even those, that isn't defined in TagSupport
        :return: Dict with all File Tag Information
        """
        return self.audio_file.tags  # TODO: This can be used directly if it's not reused

    # TODO: make @staticmethod, pass filepath directly to this function
    def readTag(self) -> Dict[str, any]:
        """
        Returns selected Tag Information defined in TagSupport
        :return: Dict with defined Tag Information
        """
        wanted_tag = dict({})
        for tag in TAGLIB_INTERNAL_NAMES.keys():
            if not self.audio_file.tags.get(tag):  # TODO: if-construct unnecessary, get already returns None
                wanted_tag[tag] = None
            else:
                wanted_tag[tag] = self.audio_file.tags.get(tag)  # TODO: use internal names, right now Taglib's internal names are used <-(- use TagSupport.getInternalName())
        return wanted_tag  # TODO: length information missing

    def writeTag(self, **kwargs) -> None:
        """
        Writes given Information to Tag assuming that it is defined in TagSupport
        :param kwargs: tag Keys and Values
        :return: None
        """
        for key, value in TAGLIB_INTERNAL_NAMES:
            if key in kwargs.keys():
                self.audio_file.tags[key] = kwargs[key]
        # TODO: Changed tag values are never saved

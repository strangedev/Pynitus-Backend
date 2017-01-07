import taglib
from typing import Dict
from src.Data.Tagging.TagSupport import TAGLIB_INTERNAL_NAMES


def writeTag(file_path: str, **kwargs) -> None:
    """
    Writes given Information to Tag assuming that it is defined in TagSupport
    :param file_path: Path of Media File to writes Tags
    :param kwargs: tag Keys and Values (Values have to been Lists!)
    :return: None
    """
    audio_file = taglib.File(file_path)
    audio_file.tags.update(kwargs)
    audio_file.save()
    audio_file.close()


def readTag(file_path: str) -> Dict[str, any]:
    """
    Returns selected Tag Information defined in TagSupport
    :param file_path: Path to Media File to read Tags of
    :return: Dict with filled Tag Information given by Track and selected by TAGLIB_INTERNAL_NAMES
    """
    audio_file = taglib.File(file_path)
    return {key: value for key, value in audio_file.tags.items() if key in TAGLIB_INTERNAL_NAMES.keys()}

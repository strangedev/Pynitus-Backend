"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Vivian Franz

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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

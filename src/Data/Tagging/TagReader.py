"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Vivian Franz, Noah Hummel

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
from typing import Dict, List, TypeVar

from src.Data.Tagging import TagSanitizer

Strings = TypeVar("Strings", str, List[str], None)


def writeTag(file_path: str, tags: Dict[str, List[str]]) -> None:
    """
    Writes given Information to Tag assuming that it is defined in TagSupport
    :param file_path: Path of Media File to writes Tags
    :param tags: tag Keys and Values
    :return: None
    """
    audio_file = taglib.File(file_path)
    audio_file.tags.update(tags)
    audio_file.save()  # FIXME: Not working!
    audio_file.close()


def readTag(file_path: str) -> Dict[str, any]:
    """
    Returns selected Tag Information defined in TagSupport
    :param file_path: Path to Media File to read Tags of
    :return: Dict with filled Tag Information given by Track and selected by TAGLIB_INTERNAL_NAMES
    """
    audio_file = taglib.File(file_path)

    tags = dict(audio_file.tags)
    tags["LENGTH"] = [str(audio_file.length)]  # Fix to make taglib behave consistently with TagSupport
    # writeTag(file_path, tags)

    return TagSanitizer.sanitizeTags(tags)

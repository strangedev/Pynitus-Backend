"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

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

from typing import List


class TagUnsupportedException(Exception):
    def __init__(self, message):
        self.message = message

TAGLIB_DISPLAY_NAMES = {
    "ARTIST": "Artist",  # type: str
    "ALBUM": "Album",  # type: str,
    "TITLE": "Title",  # type: str
    "SUBTITLE": "Subtitle",  # type: str
    "ALBUMARTIST": "Album Artist",  # type: str
    "CONDUCTOR": "Conductor",  # type: str
    "REMIXER": "Remixer",  # type: str
    "COMPOSER": "Composer",  # type: str
    "LYRICIST": "Lyricist",  # type: str
    "FEATURES": "Featuring",  # type: List[str]
    "TRACKNUMBER": "Track number",  # type: str
    "LABEL": "Label",  # type: str
    "GENRE": "Genres",  # type: List[str]
    "DATE": "Date",  # type: str
    "BPM": "Beats per minute",  # type: str
    "KEY": "Musical key",  # type: str
    "MOOD": "Mood",  # type: str
    "LENGTH": "Length (s)",  # type: str
    "COMMENT": "Comment",  # type: str
}

TAGLIB_INTERNAL_NAMES = {
    "ARTIST": "artist",  # type: str
    "ALBUM": "album",  # type: str,
    "TITLE": "title",  # type: str
    "SUBTITLE": "subtitle",  # type: str
    "ALBUMARTIST": "album_artist",  # type: str
    "CONDUCTOR": "conductor",  # type: str
    "REMIXER": "remixer",  # type: str
    "COMPOSER": "composer",  # type: str
    "LYRICIST": "lyricist",  # type: str
    "FEATURES": "features",  # type: List[str]
    "TRACKNUMBER": "track_number",  # type: str
    "LABEL": "label",  # type: str
    "GENRE": "genres",  # type: List[str]
    "DATE": "date",  # type: str
    "BPM": "bpm",  # type: str
    "KEY": "key",  # type: str
    "MOOD": "mood",  # type: str
    "LENGTH": "length",  # type: str
    "COMMENT": "comment",  # type: str
}

TAGLIB_IDENTIFIER_LOOKUP = {
    "artist": "ARTIST",  # type: str
    "album": "ALBUM",  # type: str,
    "title": "TITLE",  # type: str
    "subtitle": "SUBTITLE",  # type: str
    "album_artist": "ALBUMARTIST",  # type: str
    "conductor": "CONDUCTOR",  # type: str
    "remixer": "REMIXER",  # type: str
    "composer": "COMPOSER",  # type: str
    "lyricist": "LYRICIST",  # type: str
    "features": "FEATURES",  # type: List[str]
    "track_number": "TRACKNUMBER",  # type: str
    "label": "LABEL",  # type: str
    "genres": "GENRE",  # type: List[str]
    "date": "DATE",  # type: str
    "bpm": "BPM",  # type: str
    "key": "KEY",  # type: str
    "mood": "MOOD",  # type: str
    "length": "LENGTH",  # type: str
    "comment": "COMMENT"  # type: str
}


def getTaglibIdentifier(attribute_name: str) -> str:
    """
    Returns the Taglib descriptor for a given internal attribute
    name.
    :raises TagUnsupportedException If the internal attribute has no supported Taglib equivalent
    :param attribute_name: The name of the internal attribute
    :return: The Taglib descriptor
    """
    if attribute_name not in TAGLIB_IDENTIFIER_LOOKUP:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(attribute_name))

    return TAGLIB_IDENTIFIER_LOOKUP[attribute_name]


def getInternalName(taglib_identifier: str) -> str:
    """
    Returns the  internal attribute name for a given Taglib descriptor
    name.
    :raises TagUnsupportedException If the tag is not supported by this software
    :param taglib_identifier: The Taglib descriptor
    :return: The internal attribute name
    """
    if taglib_identifier not in TAGLIB_INTERNAL_NAMES:
        raise TagUnsupportedException("{} is not a supported tag attribute.".format(taglib_identifier))

    return TAGLIB_INTERNAL_NAMES[taglib_identifier]


def getDisplayNameByTaglibIdentifier(taglib_identifier: str) -> str:
    """
    Returns the display name for a given Taglib descriptor
    name.
    :raises TagUnsupportedException If the tag is not supported by this software
    :param taglib_identifier: The Taglib descriptor
    :return: The display name
    """
    if taglib_identifier not in TAGLIB_DISPLAY_NAMES:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(taglib_identifier))

    return TAGLIB_DISPLAY_NAMES[taglib_identifier]


def getDisplayNameByInternalName(attribute_name: str) -> str:
    """
    Returns the display name for a given internal attribute name
    name.
    :raises TagUnsupportedException If the tag is not supported by this software
    :param attribute_name: The internal attribute name
    :return: The display name
    """
    if attribute_name not in TAGLIB_INTERNAL_NAMES:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(attribute_name))

    return TAGLIB_DISPLAY_NAMES[TAGLIB_IDENTIFIER_LOOKUP[attribute_name]]




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
from typing import List, TypeVar, GenericMeta, Set

import src.Utilities.TypingFixes  # This import is not unused, rather, it is a dirty hack to be left alone


class TagUnsupportedException(Exception):
    def __init__(self, message):
        self.message = message

TagType = TypeVar("TagType", GenericMeta, type)

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

TAGLIB_IDENTIFIER_TYPES = {
    "ARTIST": str,  # type: TagType
    "ALBUM": str,  # type: TagType
    "TITLE": str,  # type: TagType
    "SUBTITLE": str,  # type: TagType
    "ALBUMARTIST": str,  # type: TagType
    "CONDUCTOR": str,  # type: TagType
    "REMIXER": str,  # type: TagType
    "COMPOSER": str,  # type: TagType
    "LYRICIST": str,  # type: TagType
    "FEATURES": List[str],  # type: TagType
    "TRACKNUMBER": str,  # type: TagType
    "LABEL": str,  # type: TagType
    "GENRE": List[str],  # type: TagType
    "DATE": str,  # type: TagType
    "BPM": str,  # type: TagType
    "KEY": str,  # type: TagType
    "MOOD": str,  # type: TagType
    "LENGTH": str,  # type: TagType
    "COMMENT": str,  # type: TagType
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

TAGLIB_INTERNAL_NAMES_TYPES = {
    "artist": str,  # type: TagType
    "album": str,  # type: TagType
    "title": str,  # type: TagType
    "subtitle": str,  # type: TagType
    "album_artist": str,  # type: TagType
    "conductor": str,  # type: TagType
    "remixer": str,  # type: TagType
    "composer": str,  # type: TagType
    "lyricist": str,  # type: TagType
    "features": List[str],  # type: TagType
    "track_number": str,  # type: TagType
    "label": str,  # type: TagType
    "genres": List[str],  # type: TagType
    "date": str,  # type: TagType
    "bpm": str,  # type: TagType
    "key": str,  # type: TagType
    "mood": str,  # type: TagType
    "length": str,  # type: TagType
    "comment": str,  # type: TagType
}

EMPTY_SYNONYMS = {  # TODO: expand
    "",
    "N/A",
    "None",
    "Unbekannt",
    "Unknown",
    "-"
}

ALL_TYPES = {**TAGLIB_IDENTIFIER_TYPES, **TAGLIB_INTERNAL_NAMES_TYPES}

USED_PRIMITIVE_TYPES = {str}  # type: Set[TagType]

USED_LIST_TYPES = {List[t] for t in USED_PRIMITIVE_TYPES}  # type: Set[TagType]

ALL_TYPEVARS = USED_PRIMITIVE_TYPES.union(USED_LIST_TYPES)   # type: Set[TagType]

INTERNAL_NAMES = set(TAGLIB_INTERNAL_NAMES.values())

TAGLIB_IDENTIFIERS = set(TAGLIB_INTERNAL_NAMES.keys())

DISPLAY_NAMES = set(TAGLIB_DISPLAY_NAMES.values())

ALL_SUPPORTED_IDENTIFIERS = INTERNAL_NAMES.union(TAGLIB_IDENTIFIERS)

TagValue = TypeVar("TagValue", *ALL_TYPEVARS)


def getTaglibIdentifier(attribute_name: str) -> str:
    """
    Returns the Taglib descriptor for a given internal attribute
    name.
    :raises TagUnsupportedException If the internal attribute has no supported Taglib equivalent
    :param attribute_name: The name of the internal attribute
    :return: The Taglib descriptor
    """
    if attribute_name not in TAGLIB_IDENTIFIER_LOOKUP:
        raise TagUnsupportedException("{} is not a supported tag attribute.".format(attribute_name))

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
        raise TagUnsupportedException("{} is not a supported tag attribute.".format(taglib_identifier))

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
        raise TagUnsupportedException("{} is not a supported tag attribute.".format(attribute_name))

    return TAGLIB_DISPLAY_NAMES[TAGLIB_IDENTIFIER_LOOKUP[attribute_name]]


def isSupported(attribute_name: str) -> bool:
    """
    Checks whether a tag attribute is supported.
    :param attribute_name: The attribute to check (internal name or Taglib ID)
    :return: True if tag attribute is supported
    """
    return attribute_name in ALL_SUPPORTED_IDENTIFIERS


def isListType(attribute_name: str) -> bool:
    """
    Checks whether a given tag attribute is a list type (e.g. genres) or not
    :param attribute_name: The attribute to check (internal name or Taglib ID)
    :return: True if tag attribute should be represented as a list type
    """

    if not isSupported(attribute_name):
        return False

    return ALL_TYPES[attribute_name] in USED_LIST_TYPES


def getType(attribute_name: str) -> TagType:
    """
    Gets the type of a tag attribute.
    :param attribute_name: The attribute whose type to get (internal name or Taglib ID)
    :raises TagUnsupportedException When the attribute is not supported
    :return: The type of the attribute
    """
    if not isSupported(attribute_name):
        raise TagUnsupportedException("{} is not a supported tag attribute.".format(attribute_name))

    return ALL_TYPES[attribute_name]


def getPrimitiveType(attribute_name: str) -> TagType:
    """
    Gets the primitive type of a tag attribute. It returns <class 'str'> when the tag's type is str,
    but also when the tag's type is List[str].
    :param attribute_name: The attribute to check (internal name or Taglib ID)
    :raises TagUnsupportedException When the attribute is not supported
    :return: The primitive type of the tag attribute
    """
    if not isSupported(attribute_name):
        raise TagUnsupportedException("{} is not a supported tag attribute.".format(attribute_name))

    attribute_type = getType(attribute_name)

    if isListType(attribute_name):
        return attribute_type.containedTypes()[0]
    else:
        return attribute_type

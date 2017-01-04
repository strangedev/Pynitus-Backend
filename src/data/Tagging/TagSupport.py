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
    Returns the 4 letter ID3 descriptor for a given internal attribute
    name.
    :raises ID3TagUnsupportedException If the internal attribute has no supported ID3
    tag equivalent
    :param attribute_name: The name of the internal attribute
    :return: The 4 letter ID3 descriptor
    """
    if attribute_name not in TAGLIB_IDENTIFIER_LOOKUP:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(attribute_name))

    return TAGLIB_IDENTIFIER_LOOKUP[attribute_name]


def getInternalName(id3_identifier: str) -> str:
    """
    Returns the  internal attribute name for a given 4 letter ID3 descriptor
    name.
    :raises ID3TagUnsupportedException If the ID3 tag is not supported by this software
    :param id3_identifier: The 4 letter ID3 descriptor
    :return: The internal attribute name
    """
    if id3_identifier not in TAGLIB_INTERNAL_NAMES:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(id3_identifier))

    return TAGLIB_INTERNAL_NAMES[id3_identifier]


def getDisplayNameByTaglibIdentifier(id3_identifier: str) -> str:
    """
    Returns the display name for a given 4 letter ID3 descriptor
    name.
    :raises ID3TagUnsupportedException If the ID3 tag is not supported by this software
    :param id3_identifier: The 4 letter ID3 descriptor
    :return: The display name
    """
    if id3_identifier not in TAGLIB_DISPLAY_NAMES:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(id3_identifier))

    return TAGLIB_DISPLAY_NAMES[id3_identifier]


def getDisplayNameByInternalName(attribute_name: str) -> str:
    """
    Returns the display name for a given internal attribute name
    name.
    :raises ID3TagUnsupportedException If the ID3 tag is not supported by this software
    :param attribute_name: The internal attribute name
    :return: The display name
    """
    if attribute_name not in TAGLIB_INTERNAL_NAMES:
        raise TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(attribute_name))

    return TAGLIB_DISPLAY_NAMES[TAGLIB_IDENTIFIER_LOOKUP[attribute_name]]




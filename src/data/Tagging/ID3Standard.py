from typing import List


class ID3TagUnsupportedException(Exception):
    def __init__(self, message):
        self.message = message


ID3_ATTRIBUTES = [
    "TPE1",  # type: str
    "TALB",  # type: str
    "TIT2",  # type: str
    "TIT3",  # type: str
    "TPE2",  # type: str
    "TPE3",  # type: str
    "TPE4",  # type: str
    "TCOM",  # type: str
    "TEXT",  # type: str
    "IPLS",  # type: List[str]
    "TRCK",  # type: str
    "TPUB",  # type: str
    "TCON",  # type: List[str]
    "TYER",  # type: str
    "TBPM",  # type: str
    "TKEY",  # type: str
    "TMOO",  # type: str
    "TLEN",  # type: str
    "ULST",  # type: str
    "WOAR",  # type: str
    "WPUB",  # type: str
    "TFLT",  # type: str
    "COMM"  # type: str
]

ID3_DISPLAY_NAMES = {
    "TPE1": "Artist",  # type: str
    "TALB": "Album",  # type: str,
    "TIT2": "Title",  # type: str
    "TIT3": "Subtitle",  # type: str
    "TPE2": "Additional Artist",  # type: str
    "TPE3": "Additional Artist (2)",  # type: str
    "TPE4": "Additional Artist (3)",  # type: str
    "TCOM": "Composer",  # type: str
    "TEXT": "Lyricist",  # type: str
    "IPLS": "Involved people",  # type: List[str]
    "TRCK": "Track number",  # type: str
    "TPUB": "Publisher",  # type: str
    "TCON": "Genres",  # type: List[str]
    "TYER": "Year",  # type: str
    "TBPM": "Beats per minute",  # type: str
    "TKEY": "Musical key",  # type: str
    "TMOO": "Mood",  # type: str
    "TLEN": "Length (ms)",  # type: str
    "ULST": "Lyrics",  # type: str
    "WOAR": "Artist URL",  # type: str
    "WPUB": "Publisher URL",  # type: str
    "TFLT": "File type",  # type: str
    "COMM": "User comment",  # type: str
}

ID3_INTERNAL_NAMES = {
    "TPE1": "artist",  # type: str
    "TALB": "album",  # type: str,
    "TIT2": "title",  # type: str
    "TIT3": "subtitle",  # type: str
    "TPE2": "additional_artist",  # type: str
    "TPE3": "additional_artist_2",  # type: str
    "TPE4": "additional_artist_3",  # type: str
    "TCOM": "composer",  # type: str
    "TEXT": "lyricist",  # type: str
    "IPLS": "involved_people",  # type: List[str]
    "TRCK": "track_number",  # type: str
    "TPUB": "publisher",  # type: str
    "TCON": "genres",  # type: List[str]
    "TYER": "year",  # type: str
    "TBPM": "bpm",  # type: str
    "TKEY": "key",  # type: str
    "TMOO": "mood",  # type: str
    "TLEN": "length",  # type: str
    "ULST": "lyrics",  # type: str
    "WOAR": "artist_url",  # type: str
    "WPUB": "publisher_url",  # type: str
    "TFLT": "file_type",  # type: str
    "COMM": "user_comment",  # type: str
}

ID3_TAG_IDENTIFIER_LOOKUP = {
    "artist": "TPE1",  # type: str
    "album": "TALB",  # type: str,
    "title": "TIT2",  # type: str
    "subtitle": "TIT3",  # type: str
    "additional_artist": "TPE2",  # type: str
    "additional_artist_2": "TPE3",  # type: str
    "additional_artist_3": "TPE4",  # type: str
    "composer": "TCOM",  # type: str
    "lyricist": "TEXT",  # type: str
    "involved_people": "IPLS",  # type: List[str]
    "track_number": "TRCK",  # type: str
    "Publisher": "TPUB",  # type: str
    "genres": "TCON",  # type: List[str]
    "year": "TYER",  # type: str
    "bpm": "TBPM",  # type: str
    "key": "TKEY",  # type: str
    "mood": "TMOO",  # type: str
    "length": "TLEN",  # type: str
    "lyrics": "ULST",  # type: str
    "artist_url": "WOAR",  # type: str
    "publisher_url": "WPUB",  # type: str
    "file_type": "TFLT",  # type: str
    "user_comment": "COMM",  # type: str
}


def getID3Identifier(attribute_name: str) -> str:
    """
    Returns the 4 letter ID3 descriptor for a given internal attribute
    name.
    :raises ID3TagUnsupportedException If the internal attribute has no supported ID3
    tag equivalent
    :param attribute_name: The name of the internal attribute
    :return: The 4 letter ID3 descriptor
    """
    if attribute_name not in ID3_TAG_IDENTIFIER_LOOKUP:
        raise ID3TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(attribute_name))

    return ID3_TAG_IDENTIFIER_LOOKUP[attribute_name]


def getInternalName(id3_identifier: str) -> str:
    """
    Returns the  internal attribute name for a given 4 letter ID3 descriptor
    name.
    :raises ID3TagUnsupportedException If the ID3 tag is not supported by this software
    :param id3_identifier: The 4 letter ID3 descriptor
    :return: The internal attribute name
    """
    if id3_identifier not in ID3_INTERNAL_NAMES:
        raise ID3TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(id3_identifier))

    return ID3_INTERNAL_NAMES[id3_identifier]


def getDisplayNameByID3Identifier(id3_identifier: str) -> str:
    """
    Returns the display name for a given 4 letter ID3 descriptor
    name.
    :raises ID3TagUnsupportedException If the ID3 tag is not supported by this software
    :param id3_identifier: The 4 letter ID3 descriptor
    :return: The display name
    """
    if id3_identifier not in ID3_DISPLAY_NAMES:
        raise ID3TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(id3_identifier))

    return ID3_DISPLAY_NAMES[id3_identifier]


def getDisplayNameByInternalName(attribute_name: str) -> str:
    """
    Returns the display name for a given internal attribute name
    name.
    :raises ID3TagUnsupportedException If the ID3 tag is not supported by this software
    :param attribute_name: The internal attribute name
    :return: The display name
    """
    if attribute_name not in ID3_INTERNAL_NAMES:
        raise ID3TagUnsupportedException("{} is not a supported ID3 tag attribute.".format(attribute_name))

    return ID3_DISPLAY_NAMES[ID3_TAG_IDENTIFIER_LOOKUP[attribute_name]]




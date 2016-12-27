from typing import Dict
from typing import List

ID3_ATTRIBUTES = {
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
    "TRCK": "Track number",  # type:
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
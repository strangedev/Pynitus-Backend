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

import io
from typing import Set, Dict
from typing import TypeVar, Type

from src.Data.Tagging import TagSanitizer
from src.Data.Tagging import TagSupport
from src.Data.Tagging.TagSupport import TagValue
from src.Data.Upload.UploadHandlers.AUploadHandler import AUploadHandler
from src.Utilities.TypingFixes import Either


class Upload(object):

    UrlArgument = TypeVar("UrlArgument", str)
    FileArgument = TypeVar("FileArgument", io.RawIOBase)

    argument_types = {
        UrlArgument,
        FileArgument
    }  # type: Set[Type[UploadArgument]]

    UploadArgument = Either(*argument_types)

    def __init__(self, upload_handler: AUploadHandler):
        self.__upload_handler = upload_handler
        self.__location = None
        self.__track_type = None
        self.__tag_info = None

    @property
    def argument_type(self) -> Type[UploadArgument]:
        return self.__upload_handler.argument_type

    @property
    def display_name(self) -> str:
        return self.__upload_handler.display_name

    @property
    def description(self) -> str:
        return self.__upload_handler.description

    @property
    def location(self) -> str:
        return self.__location

    @property
    def track_type(self):
        return self.__track_type

    @property
    def tag_info(self):
        return self.__tag_info

    @tag_info.setter
    def tag_info(self, tag_info: Dict[str, TagValue]):
        tag_info = TagSanitizer.sanitizeTags(tag_info)
        self.__tag_info = tag_info

    def handle(self, upload_argument: UploadArgument):
        self.__location, self.__track_type, self.__tag_info = self.__upload_handler.handle(upload_argument)

    @property
    def required_metadata_resent(self):
        return all([bool(self.__tag_info[x]) for x in TagSupport.REQUIRED_TAGS])

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
from typing import Dict
from typing import Set

from src.Data.Upload.UploadHandlerDescription import UploadHandlerDescription
from src.Data.Upload.Upload import Upload
from src.Data.Upload.UploadHandlers.AUploadHandler import AUploadHandler
from src.Data.Upload.UploadHandlers.YoutubeUploadHandler import YoutubeUploadHandler
from src.Database.Database import Database


class NoUploadHandlerException(Exception):
    def __init__(self, message):
        self.message = message


class DatabaseNotConnectedException(Exception):
    def __init__(self):
        self.message = "No database was connected to UploadBroker, but an upload was requested to be imported into " \
                       "the database."


class UploadInvalidException(Exception):
    def __init__(self):
        self.message = "The required metadata was not provided, a track could not be imported."


class UploadBroker(object):

    __upload_handlers = {}  # type: Dict[str, AUploadHandler]
    __database = None  # type: Database

    @classmethod
    def getUploadHandlerDescriptions(cls) -> Set[UploadHandlerDescription]:
        return sorted(set([UploadHandlerDescription(name, handler.display_name, handler.description)
                           for name, handler in UploadBroker.__upload_handlers.items()]))

    @classmethod
    def registerUploadHandler(cls, upload_handler: AUploadHandler.__class__) -> None:
        UploadBroker.__upload_handlers[upload_handler.__name__] = upload_handler

    @classmethod
    def connectDatabase(cls, database: Database) -> None:
        UploadBroker.__database = database

    @staticmethod
    def getUpload(upload_internal_handler_name: str) -> Upload:
        if upload_internal_handler_name not in UploadBroker.__upload_handlers:
            raise NoUploadHandlerException("No UploadHandler was registered for {}, but an Upload was requested."
                                           .format(upload_internal_handler_name))
        return Upload(UploadBroker.__upload_handlers[upload_internal_handler_name])

    @staticmethod
    def importIntoDatabase(upload: Upload) -> None:
        if UploadBroker.__database is None:
            raise DatabaseNotConnectedException()
        if not upload.required_metadata_resent:
            raise UploadInvalidException()

        UploadBroker.__database.addTrack(upload.location, upload.track_type, upload.tag_info)

UploadBroker.registerUploadHandler(YoutubeUploadHandler)
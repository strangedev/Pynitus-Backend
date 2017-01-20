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

from typing import Tuple, Dict

from src.Data.Tagging.TagSupport import TagValue
from src.Data.Upload.Upload import Upload


class AUploadHandler(object):
    """
    Abstract class for all supported UploadHandlers.
    An UploadHandler is a class responsible for processing the upload of a track to the server, after the
    required data was sent to the server by the user.

    It specifies a type for an argument which will be entered by the user at the upload page for
    the UploadHandler.

    When you implement a new UploadHandler class (for example YourUploadHandler), register it with UploadBroker to make
    it visible to the software:

        UploadBroker.registerUploadHandler(YourUploadHandler)

    Gotcha: Pass your UploadHandler CLASS not an INSTANCE of it:

        UploadBroker.registerUploadHandler(YourUploadHandler())  # WRONG!

        my_handler = YourUploadHandler()  # WRONG!
        UploadBroker.registerUploadHandler(my_handler)  # WRONG!

    """

    """
    The type of the upload argument.
    The supported types can be obtained from Upload.argument_types.
    Any types not listed there are not supported by the front end and will result in errors if used.
    The generic type for all supported upload arguments is UploadArgument.
    """
    argument_type = None  # type: Upload.UploadArgument

    """
    A human-readable name for the Upload Handler. It should be the same as the name of the source the
    UploadHandler can handle. If , for example, an UploadHandler is capable of handling Free Music Archive urls,
    it should be named "Free Music Archive".
    This name will be shown to the user on the upload page, when all available sources are listed.
    """
    display_name = "Abstract"

    """
    A human-readable description of when the UploadHandler should be chosen by the user and what it's limits are.
    This description will be shown to the user to help them decide which UploadHandler to use.
    """
    description = "An abstract UploadHandler. If you see this, someone screwed up the code."

    @classmethod
    def handle(cls, upload_argument: Upload.UploadArgument) -> Tuple[str, str, Dict[str, TagValue]]:
        """
        Handles the data the user entered as the tracks upload_argument.(e.g. URL string, uploaded file, etc.)
        The type of the argument is given by argument_type.

        This method should perform any steps the associated Track class
        needs to be functional (e.g saving an uploaded file to disk, downloading
        an audio file from a streaming resource)

        This function must return a tuple (location, track_type, tag_info) containing all required information
        to add the track to the database. This information includes:

            location: The location of the associated resource. This must be a unique identifier, as it is used in the
                database as a primary key. The resource has to be meaningful only to the associated Track class.
                (File path for local files, url for streaming resources, etc.)
                If it is not needed by the Track class, it may just be a unique string, although this is not
                recommended, because separate UploadHandlers can't easily guarantee uniqueness of location.
            track_type: Name of the associated Track class (the Track class the upload should result in)
            tag_info: A dictionary containing track meta information according to TagSupport. The user will
                be presented with this data and asked to fill in missing or incorrect fields. Make sure to
                give your best effort when creating this dict, as it greatly improves user experience.
                The user will be asked to fill out at least artist, album and title.

        The track_type may be altered to any suiting class, for example an upload handler for SoundCloud may result
        in a FileTrack, if the track is downloaded to a local file.

        :param upload_argument: The argument entered by the user during the upload
        :return: A tuple containing the uploaded track's information as described above.
        """
        return NotImplemented

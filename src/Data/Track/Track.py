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

from src.Data.Tagging import TagSanitizer
from src.Data.Tagging import TagSupport
from src.Data.Tagging.TagSupport import TagValue
from src.Player.PlaybackHandler import PlaybackHandler


class Track(object):
    """
    Superclass for all playable and manageable Tracks.
    """

    name = "Track"
    description = "A Track"

    def __init__(self, location: str):

        self.playback_handler_class = PlaybackHandler
        self.playback_handler_instance = None  # TODO: Move to central PlaybackHandler
        self.delegate = None

        self.location = location

        self.title = None
        self.artist = None
        self.album = None
        self.subtitle = None
        self.album_artist = None
        self.conductor = None
        self.remixer = None
        self.composer = None
        self.lyricist = None
        self.features = None
        self.track_number = None
        self.label = None
        self.genres = None
        self.date = None
        self.bpm = None
        self.key = None
        self.mood = None
        self.length = None
        self.comment = None

    @property
    def tag_info(self):
        return {key: getattr(self, key) for key in TagSupport.INTERNAL_NAMES}

    @tag_info.setter
    def tag_info(self, tag_info: Dict[str, TagValue]):

        tag_info = TagSanitizer.sanitizeTags(tag_info)

        for key in TagSupport.TAGLIB_INTERNAL_NAMES.values():
            setattr(self, key, tag_info[key])

    def play(self, delegate: object):
        """
        Instatiates the playbackHandlerClass and starts
        playback.

        Calls the delegates onFinished() method once playback is done.
        Calls the delegates onStopped() method once playback is stopped
        by stop().
        """

        self.playback_handler_instance = self.playback_handler_class()
        self.playback_handler_instance.play(self, delegate)

    def stop(self):
        """
        Stops the playback using the playbackHandlerClass's
        stop() method.
        """

        self.playback_handler_instance.stop()
        del self.playback_handler_instance

    def onFinished(self):
        self.delegate.onFinished()

    def onStopped(self):
        self.delegate.onStopped()

    def available(self) -> bool:
        """
        Checks if the resource is available and the track can be played
        back. This method is called regularly and on startup. It should
        return true if the track can be played. If this method returns false,
        the associated track is not shown to the user and the admin is asked
        to perform some kind of action to fix the issue.

        :return: A bool indicating whether the track can be played.
        """
        return False

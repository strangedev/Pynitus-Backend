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

from src.Data.Track.PlaybackHandler import PlaybackHandler


def lazy_metadata(func):
    def wrapper(self, *args, **kwargs):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return func(self, *args, **kwargs)
    return wrapper


class Track(object):
    """
    Superclass for all playable and manageable Tracks.
    """

    description = "A Track"

    def __init__(self, title: str, artist: str, album: str):

        self.playback_handler_class = PlaybackHandler
        self.playback_handler_instance = None  # TODO: Move to central PlaybackHandler
        self.delegate = None
        self.__meta_info_loaded = False
        self.__meta_info_load_hook = None

        self.__title = title
        self.__artist = artist
        self.__album = album
        self.__subtitle = None
        self.__album_artist = None
        self.__conductor = None
        self.__remixer = None
        self.__composer = None
        self.__lyricist = None
        self.__features = None
        self.__track_number = None
        self.__label = None
        self.__genres = None
        self.__date = None
        self.__bpm = None
        self.__key = None
        self.__mood = None
        self.__length = None
        self.__comment = None

    @property
    def meta_info_load_hook(self):
        return None

    @meta_info_load_hook.setter
    def meta_info_load_hook(self, hook):
        self.__meta_info_load_hook = hook

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def artist(self):
        return self.__artist

    @artist.setter
    def artist(self, artist):
        self.__artist = artist

    @property
    def album(self):
        return self.__album

    @album.setter
    def album(self, album):
        self.__album = album

    @property
    def subtitle(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__subtitle

    @subtitle.setter
    def subtitle(self, subtitle):
        self.__subtitle = subtitle

    @property
    def album_artist(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__album_artist

    @album_artist.setter
    def album_artist(self, album_artist):
        self.__album_artist = album_artist

    @property
    def conductor(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__conductor

    @conductor.setter
    def conductor(self, conductor):
        self.__conductor = conductor

    @property
    def remixer(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__remixer

    @remixer.setter
    def remixer(self, remixer):
        self.__remixer = remixer

    @property
    def composer(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__composer

    @composer.setter
    def composer(self, composer):
        self.__composer = composer

    @property
    def lyricist(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__lyricist

    @lyricist.setter
    def lyricist(self, lyricist):
        self.__lyricist = lyricist

    @property
    def features(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__features

    @features.setter
    def features(self, features):
        self.__features = features

    @property
    def track_number(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__track_number

    @track_number.setter
    def track_number(self, track_number):
        self.__track_number = track_number

    @property
    def label(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__label

    @label.setter
    def label(self, label):
        self.__label = label

    @property
    def genres(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__genres

    @genres.setter
    def genres(self, genres):
        self.__genres = genres

    @property
    def date(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def bpm(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__bpm

    @bpm.setter
    def bpm(self, bpm):
        self.__bpm = bpm

    @property
    def key(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def mood(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__mood

    @mood.setter
    def mood(self, mood):
        self.__mood = mood

    @property
    def length(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__length

    @length.setter
    def length(self, length):
        self.__length = length

    @property
    def comment(self):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return self.__comment

    @comment.setter
    def comment(self, comment):
        self.__comment = comment

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

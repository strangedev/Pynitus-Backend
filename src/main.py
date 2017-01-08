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

import os
import sys

from src.Config.ConfigLoader import ConfigLoader
from src.Data.MusicLibrary import MusicLibrary
from src.Data.PlaybackQueue import PlaybackQueue
from src.Data.Track.TrackFactory import TrackFactory
from src.Server.RESTHandler import RESTHandler


def __main__(args):

    if len(args) < 2:
        raise Exception("Specify a working directory.")

    working_dir = args[1]

    if not os.path.isdir(working_dir):
        raise Exception("Working directory is not a directory.")

    config = ConfigLoader(working_dir)
    music_library = MusicLibrary(config)
    playback_queue = PlaybackQueue()
    track_factory = TrackFactory()
    RESTHandler(
        config, playback_queue, music_library, track_factory
    )

    print("Artists:")
    print(music_library.getArtists())
    print("\n")

    print("Albums:")
    print(music_library.getAlbums())
    print("\n")

    print("Tracks:")
    print(music_library.getTracks())
    print("\n")

__main__(sys.argv)
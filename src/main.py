import os
import sys

from src.config.ConfigLoader import ConfigLoader
from src.data.MusicLibrary import MusicLibrary
from src.data.PlaybackQueue import PlaybackQueue
from src.data.Track.TrackFactory import TrackFactory
from src.server.RESTHandler import RESTHandler


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
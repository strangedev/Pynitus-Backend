import os
import sys

import ConfigLoader
import PlaybackQueue
from data import MusicLibrary
from data.Track import TrackFactory
from server import RESTHandler


def __main__(args):

    if len(args) < 2:
        raise Exception("Specify a working directory.")

    workingDir = args[1]

    if not os.path.isdir(workingDir):
        raise Exception("Working directory is not a directory.")

    config = ConfigLoader.ConfigLoader(workingDir)
    musicLibrary = MusicLibrary.MusicLibrary(config)
    playbackQueue = PlaybackQueue.PlaybackQueue()
    trackFactory = TrackFactory.TrackFactory()
    restHandler = RESTHandler.RESTHandler(
        config, playbackQueue, musicLibrary, trackFactory
    )

    # musicLibrary.addArtist("Panflöten Peter")
    # musicLibrary.addAlbum("Panflöten Peter", "Flöten aus meiner Seele")
    # musicLibrary.addTrack("Panflöten Peter", "Flöten aus meiner Seele", "Flötensolo, Duett in Z Moll")

    # print(musicLibrary.getAlbumsForArtist("Panflöten Peter"))
    # print(musicLibrary.getTracksForAlbumOfArtist("Panflöten Peter", "Flöten aus meiner Seele"))
    # print(musicLibrary.getTracksForArtist("Panflöten Peter"))

    print("Artists:")
    print(musicLibrary.getArtists())
    print("\n")

    print("Albums:")
    print(musicLibrary.getAllAlbums())
    print("\n")

    print("Tracks:")
    print(musicLibrary.getAllTracks())
    print("\n")

    # musicPlayer = MusicPlayer.MusicPlayer(musicLibrary)
    # musicPlayer.startPlaying("/home/strange/test.mp3")
    # time.sleep(3)

    # musicPlayer.stopPlaying()

    #musicLibrary.artists["Porcupine Tree"].albums["In Absentia"].tracks["05 - Gravity Eyelids"].play(DummyHandler())
    # time.sleep(3)
    #musicLibrary.artists["Porcupine Tree"].albums["In Absentia"].tracks["05 - Gravity Eyelids"].stop()

    #theTrack = musicLibrary.artists["A Perfect Circle"].albums["Stone and Echo"].tracks["Full Album"]
    # playbackQueue.addToQueue(musicLibrary.artists["Marst"]\
    #					   	.albums["Unsorted"]\
    #					  	.tracks["Aquamour"]
    #					  	)
    # playbackQueue.addToQueue(musicLibrary.artists["Unsorted"]\
    #					   	.albums["Unsorted"]\
    #					  	.tracks["test"]
    #					  	)
    # playbackQueue.addToQueue(musicLibrary.artists["A Perfect Circle"]\
    #					   	.albums["Stone and Echo"]\
    #					  	.tracks["Full Album"]
    #					  	)

    # playbackQueue.startPlaying()
    # time.sleep(4)
    # playbackQueue.playNext()
    # time.sleep(4)
    # playbackQueue.stopPlaying()
    # print(playbackQueue.getQueued())
    # time.sleep(4)
    # playbackQueue.startPlaying()
    # time.sleep(4)
    # playbackQueue.playPrevious()
    # time.sleep(4)
    # playbackQueue.stopPlaying()


__main__(sys.argv)
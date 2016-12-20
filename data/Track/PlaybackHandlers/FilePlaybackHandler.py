class FilePlaybackHandler(PlaybackHandler):
    """
    A PlaybackHandler capable of playing back local
    audio files.
    """

    def __init__(self):
        super().__init__()

    def play(self, track, delegate: object) -> None:
        if self.isPlaying():
            return

        playerCommand = ["mplayer", track.filepath]

        super().play(playerCommand, delegate)
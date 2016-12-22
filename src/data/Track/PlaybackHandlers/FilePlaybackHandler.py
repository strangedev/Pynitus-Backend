from src.data.Track import PlaybackHandler


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

        player_command = ["mplayer", track.filepath]

        super().play(player_command, delegate)
from src.data.Track import PlaybackHandler


class YoutubePlaybackHandler(PlaybackHandler):
    """
    A PlaybackHandler capable of playing back sound
    from youtube videos.
    """

    def __init__(self):
        super().__init__()

    def play(self, track, delegate: object) -> None:
        if self.isPlaying():
            return

        player_command = ["mpv", "--vid=no", track.url]

        super().play(player_command, delegate)

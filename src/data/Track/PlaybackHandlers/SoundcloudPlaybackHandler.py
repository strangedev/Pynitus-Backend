from src.data import PlaybackHandler


class SoundcloudPlaybackHandler(PlaybackHandler):
    """
    A PlaybackHandler capable of playing back sound
    from youtube videos.
    """

    def __init__(self):
        super().__init__()

    def play(self, track, delegate: object) -> None:
        if self.isPlaying():
            return

        player_command = ["mpv", track.url]

        super().play(player_command, delegate)
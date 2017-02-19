from Pynitus.framework.pubsub import sub
from Pynitus.player.player import Player
from Pynitus.pools.queue import queue
from Pynitus.model import tracks

player = Player()


def play_next() -> None:
    player.stop()

    queue.next()
    next_track = tracks.get(queue.current)

    if next_track is not None:
        player.play(next_track.mrl)

sub("vote_passed", play_next)
sub("track_ended", play_next)


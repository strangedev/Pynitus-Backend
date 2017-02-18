from Pynitus.Pynitus.framework.pubsub import sub

from Pynitus.Pynitus.model.library import get
from Pynitus.Pynitus.player.player import Player
from Pynitus.Pynitus.pools.queue import queue

player = Player()


def play_next() -> None:
    player.stop()

    queue.next()
    next_track = get(queue.current)

    if next_track is not None:
        player.play(next_track.mrl)

sub("vote_passed", play_next)
sub("track_ended", play_next)


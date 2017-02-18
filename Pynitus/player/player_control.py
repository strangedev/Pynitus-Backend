from pubsub import pub

from Pynitus.player.player import Player
from Pynitus.pools.library import get
from Pynitus.pools.queue import queue

player = Player()


def play_next() -> None:
    player.stop()

    queue.next()
    next_track = get(queue.current)

    if next_track is not None:
        player.play(next_track.mrl)


pub.subscribe(play_next, "vote_passed")
pub.subscribe(play_next, "track_ended")


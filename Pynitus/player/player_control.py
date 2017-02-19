from Pynitus.framework.pubsub import sub
from Pynitus.model import tracks
from Pynitus.player.queue import queue
from Pynitus import pluggable


player = None


def play_next() -> None:
    player.stop()

    queue.next()
    next_track = tracks.get(queue.current)

    if next_track is not None:
        prepare_backend(next_track.status.backend)
        player.play(next_track.mrl)


def prepare_backend(backend: str) -> bool:
    global player

    if backend not in pluggable.backends.keys():
        return False

    player = pluggable.backends[backend]

    initialized = False

    if hasattr(player, "initialized"):
        initialized = player.initialized

    if not initialized:
        player.init(play_next)
        setattr(player, "initialized", True)

    return True


sub("vote_passed", play_next)
sub("track_ended", play_next)

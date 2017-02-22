from tinnitus import remote

from Pynitus.framework.pubsub import sub


def init_player():
    sub("player.play", play)
    sub("player.pause", pause)
    sub("player.stop", stop)


def get_status():
    with remote() as r:
        status = r.status()
    return status


def play():
    with remote() as r:
        r.play()


def play_next():
    with remote() as r:
        r.play_next()


def pause():
    with remote() as r:
        r.pause()


def stop():
    with remote() as r:
        r.stop()


def available(mrl, backend) -> bool:
    available = True
    with remote() as r:
        available = r.available(mrl, backend)

    return available != False
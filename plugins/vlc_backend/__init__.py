from typing import Callable

import vlc


__vlc_instance = None
__player = None
__stopped = True
__paused = False
__playback_end_callback = lambda: NotImplemented


def init(playback_end_callback: Callable[None]) -> None:
    global __vlc_instance
    global __player
    global __playback_end_callback

    __vlc_instance = vlc.Instance("--no-xlib")
    __player = __vlc_instance.media_player_new()
    __playback_end_callback = playback_end_callback
    __player.event_manager().event_attach(
        vlc.EventType.MediaPlayerEndReached,
        playback_end_callback
    )


def play(mrl: str) -> None:
    global __stopped
    global __paused

    if __paused:
        __player.pause()

    elif __stopped:
        __player.set_mrl(mrl)
        __player.play()
        if not __player.will_play():
            __playback_end_callback()
            __player.stop()
            return

    __stopped = False
    __paused = False


def stop() -> None:
    global __stopped
    global __paused

    if (not __stopped) and __paused:
            __player.pause()
            __player.stop()

    __stopped = True
    __paused = False


def pause() -> None:
    if (not __stopped) and (not __paused):
        __player.pause()

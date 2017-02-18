import vlc
from pubsub import pub


class Player(object):

    def __init__(self):
        self.__vlc_instance = vlc.Instance("--no-xlib")
        self.__player = self.__vlc_instance.media_player_new()
        self.__player.event_manager().event_attach(
            vlc.EventType.MediaPlayerPlaying,
            lambda instance: pub.sendMessage("track_ended")
        )
        self.__stopped = True
        self.__paused = False

    def play(self, mrl: str) -> None:
        if self.__paused:
            self.__player.pause()

        elif self.__stopped:
            self.__player.set_mrl(mrl)
            self.__player.play()
            if not self.__player.will_play():
                pub.sendMessage("track_ended")
                self.__player.stop()
                return

        self.__stopped = False
        self.__paused = False

    def stop(self) -> None:
        if not self.__stopped:
            if self.__paused:
                self.__player.pause()
            self.__player.stop()

        self.__stopped = True
        self.__paused = False

    def pause(self) -> None:
        if not self.__stopped and not self.__paused:
            self.__player.pause()

    @property
    def playing(self):
        return not self.__paused and not self.__stopped

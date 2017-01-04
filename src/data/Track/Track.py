from src.data.Track.PlaybackHandler import PlaybackHandler


def lazy_metadata(func):
    def wrapper(self, *args, **kwargs):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return func(self, *args, **kwargs)
    return wrapper


class Track(object):
    """
    Superclass for all playable and manageable Tracks.
    """

    description = "A Track"

    def __init__(self, title: str, artist: str, album: str):

        self.playback_handler_class = PlaybackHandler
        self.playback_handler_instance = None  # TODO: Move to central PlaybackHandler
        self.delegate = None
        self.__meta_info_loaded = False
        self.__meta_info_load_hook = None

        self.title = title
        self.artist = artist
        self.album = album

    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, title):
        self.title = title

    @property
    def artist(self):
        return self.artist

    @artist.setter
    def artist(self, artist):
        self.artist = artist

    @property
    def album(self):
        return self.album

    @album.setter
    def album(self, album):
        self.album = album

    @property
    @lazy_metadata
    def subtitle(self):
        return self.subtitle

    @subtitle.setter
    def subtitle(self, subtitle):
        self.subtitle = subtitle

    @property
    @lazy_metadata
    def album_artist(self):
        return self.album_artist

    @album_artist.setter
    def album_artist(self, album_artist):
        self.album_artist = album_artist

    @property
    @lazy_metadata
    def conductor(self):
        return self.conductor

    @conductor.setter
    def conductor(self, conductor):
        self.conductor = conductor

    @property
    @lazy_metadata
    def remixer(self):
        return self.remixer

    @remixer.setter
    def remixer(self, remixer):
        self.remixer = remixer

    @property
    @lazy_metadata
    def composer(self):
        return self.composer

    @composer.setter
    def composer(self, composer):
        self.composer = composer

    @property
    @lazy_metadata
    def lyricist(self):
        return self.lyricist

    @lyricist.setter
    def lyricist(self, lyricist):
        self.lyricist = lyricist

    @property
    @lazy_metadata
    def features(self):
        return self.features

    @features.setter
    def features(self, features):
        self.features = features

    @property
    @lazy_metadata
    def track_number(self):
        return self.track_number

    @track_number.setter
    def track_number(self, track_number):
        self.track_number = track_number

    @property
    @lazy_metadata
    def label(self):
        return self.label

    @label.setter
    def label(self, label):
        self.label = label

    @property
    @lazy_metadata
    def genres(self):
        return self.genres

    @genres.setter
    def genres(self, genres):
        self.genres = genres

    @property
    @lazy_metadata
    def date(self):
        return self.date

    @date.setter
    def date(self, date):
        self.date = date

    @property
    @lazy_metadata
    def bpm(self):
        return self.bpm

    @bpm.setter
    def bpm(self, bpm):
        self.bpm = bpm

    @property
    @lazy_metadata
    def key(self):
        return self.key

    @key.setter
    def key(self, key):
        self.key = key

    @property
    @lazy_metadata
    def mood(self):
        return self.mood

    @mood.setter
    def mood(self, mood):
        self.mood = mood

    @property
    @lazy_metadata
    def length(self):
        return self.length

    @length.setter
    def length(self, length):
        self.length = length

    @property
    @lazy_metadata
    def comment(self):
        return self.comment

    @comment.setter
    def comment(self, comment):
        self.comment = comment

    def play(self, delegate: object):
        """
        Instatiates the playbackHandlerClass and starts
        playback.

        Calls the delegates onFinished() method once playback is done.
        Calls the delegates onStopped() method once playback is stopped
        by stop().
        """

        self.playback_handler_instance = self.playback_handler_class()
        self.playback_handler_instance.play(self, delegate)

    def stop(self):
        """
        Stops the playback using the playbackHandlerClass's
        stop() method.
        """

        self.playback_handler_instance.stop()
        del self.playback_handler_instance

    def onFinished(self):
        self.delegate.onFinished()

    def onStopped(self):
        self.delegate.onStopped()

    def available(self) -> bool:
        """
        Checks if the resource is available and the track can be played
        back. This method is called regularly and on startup. It should
        return true if the track can be played. If this method returns false,
        the associated track is not shown to the user and the admin is asked
        to perform some kind of action to fix the issue.

        :return: A bool indicating whether the track can be played.
        """
        return NotImplemented

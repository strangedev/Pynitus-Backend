from src.data.Track.PlaybackHandler import PlaybackHandler


def lazy_metadata(func):
    def wrapper(self, **kwargs):
        if not self.__meta_info_loaded:
            self.__meta_info_load_hook(self)
        return func(self, **kwargs)
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
    def additional_artist(self):
        return self.additional_artist

    @additional_artist.setter
    def additional_artist(self, additional_artist):
        self.additional_artist = additional_artist

    @property
    @lazy_metadata
    def additional_artist_2(self):
        return self.additional_artist_2

    @additional_artist_2.setter
    def additional_artist_2(self, additional_artist_2):
        self.additional_artist_2 = additional_artist_2

    @property
    @lazy_metadata
    def additional_artist_3(self):
        return self.additional_artist_3

    @additional_artist_3.setter
    def additional_artist_3(self, additional_artist_3):
        self.additional_artist_3 = additional_artist_3

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
    def involved(self):
        return self.involved

    @involved.setter
    def involved(self, involved):
        self.involved = involved

    @property
    @lazy_metadata
    def track_number(self):
        return self.track_number

    @track_number.setter
    def track_number(self, track_number):
        self.track_number = track_number

    @property
    @lazy_metadata
    def publisher(self):
        return self.publisher

    @publisher.setter
    def publisher(self, publisher):
        self.publisher = publisher

    @property
    @lazy_metadata
    def genres(self):
        return self.genres

    @genres.setter
    def genres(self, genres):
        self.genres = genres

    @property
    @lazy_metadata
    def year(self):
        return self.year

    @year.setter
    def year(self, year):
        self.year = year

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
    def lyrics(self):
        return self.lyrics

    @lyrics.setter
    def lyrics(self, lyrics):
        self.lyrics = lyrics

    @property
    @lazy_metadata
    def artist_url(self):
        return self.artist_url

    @artist_url.setter
    def artist_url(self, artist_url):
        self.artist_url = artist_url

    @property
    @lazy_metadata
    def publisher_url(self):
        return self.publisher_url

    @publisher_url.setter
    def publisher_url(self, publisher_url):
        self.publisher_url = publisher_url

    @property
    @lazy_metadata
    def file_type(self):
        return self.file_type

    @file_type.setter
    def file_type(self, file_type):
        self.file_type = file_type

    @property
    @lazy_metadata
    def user_comment(self):
        return self.user_comment

    @user_comment.setter
    def user_comment(self, user_comment):
        self.user_comment = user_comment

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

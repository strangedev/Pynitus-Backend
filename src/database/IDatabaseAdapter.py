from typing import Dict, List, Any


class IDatabaseAdapter(object):
    """
    Interface class representing a database implementation.
    The database representation should implement a database capable
    of storing information precisely as described in this file.

    This interface is relied upon by Database.
    It makes Database work with different databases by encapsulating
    all database-related code within the implementing IDatabaseAdapter
    class.
    """

    def addTrack(
            self,
            location: str,
            title: str=None,
            artist: str=None,
            album: str=None,
            track_type: str=None,
            **kwargs: Dict[str, Any]
    ) -> None:
        """
        Adds a new track to the database.
        Newly added tracks are unimported by default.

        Basic information has to be fully provided
        before the track can be imported. This information includes:

        Title, Artist name, Album title, Track type (class name of corresponding
        class), Track location (a file path or url pointing to the media
        resource)

        In order to add a track to the database (information might be missing on
        automatic import) only a location has to be specified.

        Supported meta information according to ID3Standard.ID3_ATTRIBUTES can
        be passed as a dictionary. The corresponding internal names (the names
        used by this software) for ID3 attributes can be found in
        ID3Standard.ID3_INTERNAL_NAMES. Type hints are provided.
        The meta information dictionary should use the internal attribute names
        of the attributes to be associated with the track as keys and any
        information of appropriate type that should be stored in the database
        as values.

        :param title: The title of the track
        :param artist: The main artist of the track (Add. artist are placed in meta info)
        :param album: The title of the album containing this track (Same as title, if single release)
        :param track_type: The class name of the corresponding track class (e.g. FileTrack)
        :param location: A file path or url pointing to the media resource
        :param kwargs: A dictionary containing meta information as described above (optional)
        :return: None
        """
        return NotImplemented

    def getArtists(self) -> List[str]:
        """
        Returns all artist names in the database as strings.
        :return: A list of strings containing all artist names
        """
        return NotImplemented

    def getAlbums(self) -> List[str]:
        """
        Returns all album titles in the database as strings.
        :return: A list of strings containing all album titles
        """
        return NotImplemented

    def getAlbumsByArtist(self, artist: str) -> List[str]:
        """
        Returns all album titles of a given artist.
        :param artist: An artist name
        :return: A list of strings containing all album titles of the given artist.
        """
        return NotImplemented

    def getTracksByArtist(self, artist: str) -> List[Dict[str, str]]:
        """
        Returns all tracks of all albums of a given artist.

        Tracks are returned as dictionaries of their basic attributes as
        specified in addTrack.
        :param artist: An artist name
        :return: A list of dictionaries containing the basic track information.
        """
        return NotImplemented

    def getTracksByAlbum(self,
                         artist: str,
                         album: str) -> List[Dict[str, str]]:
        """
        Returns all tracks of a given album of a given artist.

        Tracks are returned as dictionaries of their basic attributes as
        specified in addTrack.
        :param artist: An artist name
        :param album: An album title
        :return: A list of dictionaries containing the basic track information.
        """
        return NotImplemented

    def getTrack(self,
                 title: str,
                 artist: str,
                 album: str) -> Dict[str, str]:
        """
        Returns a tracks by title of a given album of a given artist.

        Tracks are returned as dictionaries of their basic attributes as
        specified in addTrack.
        :param title: The track title
        :param artist: The artist name
        :param album: The album title
        :return: A dictionary containing the basic track information.
        """
        return NotImplemented

    def getUnimported(self) -> List[Dict[str, str]]:
        """
        Returns all tracks marked as unimported in the database.

        Tracks that are unimported are added to the database, but not shown
        to the user, because they lack basic information as specified in
        addTrack. The admin has the option to provide this information
        in order to import any unimported tracks at any time.

        :return: A list of dictionaries containing the basic track information.
        """
        return NotImplemented

    def getUnavailable(self) -> List[Dict[str, str]]:
        """
        Returns all tracks marked as unavailable in the database.

        Availability marks a tracks readiness to be played back.
        The availability of a track is checked on startup and when a track is added
        to the playlist. The admin has the option to check on unavailable tracks
        and take some form of action to fix the issue.

        :return: A list of dictionaries containing the basic track information.
        """
        return NotImplemented

    def getMetainformation(
            self,
            title: str,
            artist: str,
            album: str) -> Dict[str, Any]:
        """
        Returns a tracks meta information a specified in ID3Standard.ID3_ATTRIBUTES
        as a dictionary. The used dictionary keys are from ID3Standard.ID3_INTERNAL_NAMES.

        :param title: The track title
        :param artist: The artist name
        :param album: The album title
        :return: A dictionary of meta information
        """
        return NotImplemented

    def setTrackIsImported(self, title: str, artist: str, album: str) -> None:
        """
        Marks a track as imported and usable.

        :param title: The track title
        :param artist: The artist name
        :param album: The album title
        :return: None
        """
        return NotImplemented

    def setTrackIsInitialized(self, title: str, artist: str, album: str) -> None:
        """
        Marks a track as initialized (startup check was performed)

        :param title: The track title
        :param artist: The artist name
        :param album: The album name
        :return: None
        """
        return NotImplemented

    def setTrackIsAvailable(self, title: str, artist: str, album: str) -> None:
        """
        Marks a track as available (can be played back).

        :param title: The track title
        :param artist: The artist name
        :param album: The album title
        :return: None
        """
        return NotImplemented

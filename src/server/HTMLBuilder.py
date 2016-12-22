import os

import jinja2
from jinja2 import Environment

from src.data.MusicLibrary import MusicLibraryType
from src.data.PlaybackQueue import PlaybackQueueType
from src.data.Track.TrackFactory import TrackFactoryType
from src.server.FloodProtection import FloodProtectionType
from src.server.VoteHandler import VoteHandlerType


class HTMLBuilder(object):

    def __init__(
        self,
        template_path: str,
        flood_protection: FloodProtectionType,
        vote_handler: VoteHandlerType,
        playback_queue: PlaybackQueueType,
        music_library: MusicLibraryType,
        track_factory: TrackFactoryType
    ):

        self.template_path = template_path  # type: str
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path)
        )                                       # type: Environment

        self.flood_protection = flood_protection  # type: FloodProtectionType
        self.vote_handler = vote_handler  # type: VoteHandlerType
        self.playback_queue = playback_queue  # type: PlaybackQueueType
        self.music_library = music_library  # type: MusicLibraryType
        self.track_factory = track_factory  # type: TrackFactoryType

    def __render_common(self, template, ip_addr, **kwargs):
        return template.render(
            actionsLeft=self.flood_protection.actionsLeft(ip_addr),
            maxActions=self.flood_protection.maxActions,
            playbackQueue=self.playback_queue,
            voteCount=self.vote_handler.votes,
            votesRequired=self.vote_handler.getRequiredVotes(),
            playing=self.playback_queue.playing,
            **kwargs
        )

    def buildArtistsPage(self, ipAddr):

        template = self.environment.get_template("artists.html")

        return self.__render_common(
            template,
            ipAddr,
            artistNames=sorted(
                [artist for artist in self.music_library.getArtists()]
            )
        )

    def buildAlbumsPage(self, ipAddr):

        template = self.environment.get_template("albums.html")

        return self.__render_common(
            template,
            ipAddr,
            albumAndArtistNames=sorted(
                [(album, artist) for artist in self.music_library.getArtists()
                 for album in self.music_library.getAlbumsForArtist(artist)]
            )
        )

    def buildTracksPage(self, ipAddr):

        template = self.environment.get_template("tracks.html")

        return self.__render_common(
            template,
            ipAddr,
            trackAndAlbumAndArtistNames=sorted(
                [(track.title, track.albumTitle, track.artistName)
                 for track in self.music_library.getTracks()]
            )
        )

    def buildQueuePage(self, ipAddr):

        template = self.environment.get_template("queue.html")

        return self.__render_common(
            template,
            ipAddr,
            trackAndAlbumAndArtistNames=[
                (track.title, track.albumTitle, track.artistName)
                for track in self.playback_queue.getQueued()]
        )

    def buildArtistPage(self, ipAddr, artist):

        template = self.environment.get_template("artist.html")

        return self.__render_common(
            template,
            ipAddr,
            albumTitles=sorted(
                [album for album
                 in self.music_library.getAlbumsForArtist(artist)]
                ),
            trackAndAlbumTitles=sorted(
                [(track.title, track.albumTitle) for track
                 in self.music_library.getTracksForArtist(artist)]
                ),
            artistName=artist
        )

    def buildAlbumPage(self, ipAddr, artist, album):

        template = self.environment.get_template("album.html")

        return self.__render_common(
            template,
            ipAddr,
            albumTitle=album,
            artistName=artist,
            trackTitles=sorted(
                [track.title for track
                    in self.music_library.getTracksForAlbumOfArtist(
                        artist, album)]
            )
        )

    def buildTrackPage(self, ipAddr):
        pass

    def buildAddPage(self, ipAddr):

        template = self.environment.get_template("add.html")

        return self.__render_common(
            template,
            ipAddr,
            trackTypesAndDescs=sorted(
                [(trackType, self.track_factory.availableTrackTypes[
                    trackType].description) for trackType
                    in self.track_factory.availableTrackTypes]
            )
        )

    def buildUploadPage(self, ipAddr, attributes):

        template = self.environment.get_template("upload.html")

        return self.__render_common(
            template,
            ipAddr,
            attributes=sorted(attributes)
        )

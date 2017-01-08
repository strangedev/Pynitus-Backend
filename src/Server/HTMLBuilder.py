"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Dict, List

import jinja2
from jinja2 import Environment
from jinja2 import Template

from src.Data.PlaybackQueue import PlaybackQueue
from src.Data.Track.TrackFactory import TrackFactory
from src.Server.FloodProtection import FloodProtection
from src.Server.VoteHandler import VoteHandler
from src.Database.Database import Database

class HTMLBuilder(object):

    def __init__(
        self,
        template_path: str,
        flood_protection: FloodProtection,
        vote_handler: VoteHandler,
        playback_queue: PlaybackQueue,
        music_library: MusicLibrary,
        track_factory: TrackFactory
    ):

        self.template_path = template_path  # type: str
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path)
        )                                       # type: Environment

        self.flood_protection = flood_protection  # type: FloodProtection
        self.vote_handler = vote_handler  # type: VoteHandler
        self.playback_queue = playback_queue  # type: PlaybackQueue
        self.music_library = music_library  # type: MusicLibrary
        self.track_factory = track_factory  # type: TrackFactory

    def __render_common(self, template: Template, ip_address: int, **kwargs) -> str:
        return template.render(
            actionsLeft=self.flood_protection.actionsLeft(ip_address),
            maxActions=self.flood_protection.max_actions,
            playbackQueue=self.playback_queue,
            voteCount=self.vote_handler.votes,
            votesRequired=self.vote_handler.getRequiredVotes(),
            playing=self.playback_queue.playing,
            **kwargs
        )

    def buildArtistsPage(self, ip_address: int) -> str:

        template = self.environment.get_template("artists.html")

        return self.__render_common(
            template,
            ip_address,
            artistNames=sorted(
                [artist for artist in self.music_library.getArtists()]
            )
        )

    def buildAlbumsPage(self, ip_address: int) -> str:

        template = self.environment.get_template("albums.html")

        return self.__render_common(
            template,
            ip_address,
            albumAndArtistNames=sorted(
                [(album, artist) for artist in self.music_library.getArtists()
                 for album in self.music_library.getAlbumsForArtist(artist)]
            )
        )

    def buildTracksPage(self, ip_address: int) -> str:

        template = self.environment.get_template("tracks.html")

        return self.__render_common(
            template,
            ip_address,
            trackAndAlbumAndArtistNames=sorted(
                [(track.title, track.album_title, track.artist_name)
                 for track in self.music_library.getTracks()]
            )
        )

    def buildQueuePage(self, ip_address: int) -> str:

        template = self.environment.get_template("queue.html")

        return self.__render_common(
            template,
            ip_address,
            trackAndAlbumAndArtistNames=[
                (track.title, track.albumTitle, track.artistName)
                for track in self.playback_queue.getQueued()]
        )

    def buildArtistPage(self, ip_address: int, artist: str) -> str:

        template = self.environment.get_template("artist.html")

        return self.__render_common(
            template,
            ip_address,
            albumTitles=sorted(
                [album for album
                 in self.music_library.getAlbumsForArtist(artist)]
                ),
            trackAndAlbumTitles=sorted(
                [(track.title, track.album_title) for track
                 in self.music_library.getTracksForArtist(artist)]
                ),
            artistName=artist
        )

    def buildAlbumPage(self, ip_address: int, artist: str, album: str) -> str:

        template = self.environment.get_template("album.html")

        return self.__render_common(
            template,
            ip_address,
            albumTitle=album,
            artistName=artist,
            trackTitles=sorted(
                [track.title for track
                    in self.music_library.getTracksForAlbumOfArtist(
                        artist, album)]
            )
        )

    def buildTrackPage(self, ip_address: int) -> str:
        pass

    def buildAddPage(self, ip_address: int) -> str:

        template = self.environment.get_template("add.html")

        return self.__render_common(
            template,
            ip_address,
            trackTypesAndDescs=sorted(
                [(track_type, self.track_factory.availableTrackTypes[
                    track_type].description) for track_type
                    in self.track_factory.availableTrackTypes]
            )
        )

    def buildUploadPage(self, ip_address: int, attributes: Dict[str, List[str]]) -> str:

        template = self.environment.get_template("upload.html")

        return self.__render_common(
            template,
            ip_address,
            attributes=sorted(attributes)
        )

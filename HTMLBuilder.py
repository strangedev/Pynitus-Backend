import os

import jinja2


class HTMLBuilder(object):

    def __init__(
        self,
        templatePath,
        floodProtection,
        voteHandler,
        playbackQueue,
        musicLibrary
    ):

        self.templatePath = templatePath
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templatePath)
        )

        self.floodProtection = floodProtection
        self.voteHandler = voteHandler
        self.playbackQueue = playbackQueue
        self.musicLibrary = musicLibrary

    def __render_common(self, template, ipAddr, **kwargs):
        return template.render(
            actionsLeft=self.floodProtection.actionsLeft(ipAddr),
            maxActions=self.floodProtection.maxActions,
            playbackQueue=self.playbackQueue,
            voteCount=self.voteHandler.votes,
            votesRequired=self.voteHandler.getRequiredVotes(),
            playing=self.playbackQueue.playing,
            **kwargs
        )

    def buildArtistsPage(self, ipAddr):

        template = self.environment.get_template("artists.html")

        return self.__render_common(
            template,
            ipAddr,
            artistNames=sorted(
                [artist for artist in self.musicLibrary.getArtists()]
            )
        )

    def buildAlbumsPage(self, ipAddr):

        template = self.environment.get_template("albums.html")

        return self.__render_common(
            template,
            ipAddr,
            albumAndArtistNames=sorted(
                [(album, artist) for artist in self.musicLibrary.getArtists()
                    for album in self.musicLibrary.getAlbumsForArtist(artist)]
            )
        )

    def buildTracksPage(self, ipAddr):

        template = self.environment.get_template("tracks.html")

        return self.__render_common(
            template,
            ipAddr,
            trackAndAlbumAndArtistNames=sorted(
                [(track.title, track.albumTitle, track.artistName)
                    for track in self.musicLibrary.getTracks()]
            )
        )

    def buildQueuePage(self, ipAddr):

        template = self.environment.get_template("queue.html")

        return self.__render_common(
            template,
            ipAddr,
            trackAndAlbumAndArtistNames=[
                (track.title, track.albumTitle, track.artistName)
                for track in self.playbackQueue.getQueued()]
        )

    def buildArtistPage(self, ipAddr, artist):

        template = self.environment.get_template("artist.html")

        return self.__render_common(
            template,
            ipAddr,
            albumTitles=sorted(
                [album for album
                    in self.musicLibrary.getAlbumsForArtist(artist)]
                ),
            trackAndAlbumTitles=sorted(
                [(track.title, track.albumTitle) for track
                    in self.musicLibrary.getTracksForArtist(artist)]
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
                    in self.musicLibrary.getTracksForAlbumOfArtist(
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
                [(trackType, trackfactory.availableTrackTypes[
                    trackType].description) for trackType
                    in trackfactory.availableTrackTypes]
            )
        )

    def buildUploadPage(self, ipAddr, attributes):

        template = self.environment.get_template("upload.html")

        return self.__render_common(
            template,
            ipAddr,
            attributes=sorted(attributes)
        )

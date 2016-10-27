import os
import shutil

import Artist
import Album
import Track
import TrackFactory


class MusicLibrary(object):

    def __init__(self, workingDirectory):

        self.trackFactory = TrackFactory.TrackFactory()

        self.workingDirectory = workingDirectory
        self.artists = dict({})

        self.__generateIndexes()

    def __generateIndexes(self):

        for artistDir in os.listdir(self.workingDirectory):

            artistPath = os.path.join(self.workingDirectory, artistDir)
            if not os.path.isdir(artistPath):
                continue

            """
            Top level of directory contains artist folders
            """
            self.addArtist(artistDir)

            for albumDir in os.listdir(artistPath):

                albumPath = os.path.join(artistPath, albumDir)
                if not os.path.isdir(albumPath):
                    continue

                """
                There might be other kinds of albums in the future
                """
                self.addAlbum(Album.Album(albumDir, artistDir))

                for trackFilename in os.listdir(albumPath):

                    trackPath = os.path.join(albumPath, trackFilename)
                    trackName, trackContainerExtension \
                        = os.path.splitext(trackFilename)

                    maybeTrack = None

                    if trackContainerExtension == ".rec":
                        maybeTrack = self.trackFactory\
                                         .getTrackFromLocalRecord(
                                            trackPath,
                                            artistDir,
                                            albumDir,
                                            trackName
                                            )

                    if maybeTrack:
                        self.addTrack(maybeTrack)

    def getArtists(self):

        return list(self.artists.values())

    def getAlbumsForArtist(self, artist):

        if artist not in self.artists:
            raise Exception("Artist doesn't exist")

        return self.artists[artist].getAlbums()

    def getAlbums(self):

        return [item for sublist in [artist.getAlbums()
                for artist in self.getArtists()] for item in sublist]

    def getTracksForAlbumOfArtist(self, artist, album):

        if artist not in self.artists:
            raise Exception("Artist doesn't exist")

        if album not in [
                            album.title for album in
                            self.getAlbumsForArtist(artist)
                        ]:
            raise Exception("Artist has no such album.")

        return list(self.artists[artist].albums[album].getTracks())

    def getTracksForArtist(self, artist):

        if artist not in self.artists:
            raise Exception("Artist doesn't exist")

        return [
                item for sublist in
                [
                    album.getTracks()
                    for album in self.artists[artist].getAlbums()
                ]
                for item in sublist
                ]

    def getTracks(self):

        return [item for sublist in
                [
                    self.getTracksForArtist(artist.name)
                    for artist in self.getArtists()
                    ] for item in sublist
                ]

    def addArtist(self, artist):

        print("Artist exists: ", artist in self.artists)

        if artist not in self.artists:
            self.artists[artist] = Artist.Artist(artist)

    def addAlbum(self, album):

        if album.artistName not in self.artists:
            raise Exception("Artist doesn't exist")

        self.artists[album.artistName].addAlbum(album)

    def addTrack(self, track):

        if track.artistName not in self.artists:
            raise Exception("Artist doesn't exist")

        if track.albumTitle not in [
                                    album.title for album
                                    in self.getAlbumsForArtist(
                                        track.artistName)
                                    ]:
            raise Exception("Album doesn't exist")

        self.artists[track.artistName].albums[track.albumTitle].addTrack(track)

    def deleteTrack(self, track):

        trackPath = os.path.join(
            self.workingDirectory,
            track.artistName,
            track.albumTitle,
            track.title
            ) + ".rec"

        shutil.rmtree(trackPath)

        del self.artists[track.artistName]\
                .albums[track.albumTitle]\
                .tracks[track.title]

    def deleteAlbum(self, album):

        albumPath = os.path.join(
            self.workingDirectory,
            album.artistName,
            album.title
            )

        shutil.rmtree(albumPath)

        del self.artists[album.artistName].albums[album.title]

    def deleteArtist(self, artist):

        artistPath = os.path.join(self.workingDirectory, artist.name)
        shutil.rmtree(artistPath)

        del self.artists[artist.name]

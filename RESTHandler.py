import signal
import os

import cherrypy
from cherrypy.lib import auth_basic

import MusicLibrary
import TrackFactory
import PlaybackQueue
import HTMLBuilder
import VoteHandler
import SessionHandler
import Album


def htmlRelPath(config, path):
    return os.path.join(config.get("htmlDir"), path)


class RESTHandler(object):

    def __init__(self, config, playbackQueue, musicLibrary, trackFactory):
        self.config = config
        self.playbackQueue = playbackQueue
        self.musicLibrary = musicLibrary
        self.trackFactory = trackFactory
        self.HTMLBuilder = HTMLBuilder.HTMLBuilder(config.get("htmlDir"))
        self.sessionHandler = SessionHandler.SessionHandler(self.config)
        self.voteHandler = VoteHandler.VoteHandler(
            self.config,
            self.sessionHandler,
            self.playbackQueue.playNext
            )

        self.__configure()
        self.__run()

    def __configure(self):
        self.cherrypyConf = {
            self.config.get("htmlRootPath"): {
                "tools.auth_basic.on": True,
                "tools.auth_basic.realm": "PiJukebox",
                "tools.auth_basic.checkpassword": self.__checkCredentials,
                "tools.sessions.on": True
            },

            "/removeFromQueue": {
                "tools.auth_basic.on": True,
                "tools.auth_basic.realm": "localhost",
                "tools.auth_basic.checkpassword": self.__checkAdminCredentials,
                "tools.sessions.on": True
            },

            "/deleteTrack": {
                "tools.auth_basic.on": True,
                "tools.auth_basic.realm": "localhost",
                "tools.auth_basic.checkpassword": self.__checkAdminCredentials,
                "tools.sessions.on": True
            },

            "/deleteAlbum": {
                "tools.auth_basic.on": True,
                "tools.auth_basic.realm": "localhost",
                "tools.auth_basic.checkpassword": self.__checkAdminCredentials,
                "tools.sessions.on": True
            },

            "/deleteArtist": {
                "tools.auth_basic.on": True,
                "tools.auth_basic.realm": "localhost",
                "tools.auth_basic.checkpassword": self.__checkAdminCredentials,
                "tools.sessions.on": True
            },

            "/css/bootstrap.min.css": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(self.config, "css/bootstrap.min.css")
            },

            "/fonts/glyphicons-halflings-regular.eot": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(self.config, "fonts/glyphicons-halflings-regular.eot")
            },

            "/fonts/glyphicons-halflings-regular.svg": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(self.config, "fonts/glyphicons-halflings-regular.svg")
            },

            "/fonts/glyphicons-halflings-regular.ttf": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(self.config, "fonts/glyphicons-halflings-regular.ttf")
            },

            "/fonts/glyphicons-halflings-regular.woff": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(self.config, "fonts/glyphicons-halflings-regular.woff")
            },

            "/fonts/glyphicons-halflings-regular.woff2": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(self.config, "fonts/glyphicons-halflings-regular.woff2")
            },

            '/favicon.ico':
                {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(self.config, "img/pynitus_32x32.ico")
            },

            '/favicon.png':
                {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(self.config, "img/pynitus_32x32.png")
            }

        }

        cherrypy.config.update(
            {'server.socket_port': self.config.get("hostPort"),
             'log.access_file': self.config.get("accessLogfile"),
             'log.error_file': self.config.get("errorLogfile"),
             'server.socket_host': self.config.get("hostAddress")}
        )

    def __run(self):
        cherrypy.quickstart(
            self,
            self.config.get("htmlRootPath"),
            self.cherrypyConf
        )

    def __checkCredentials(self, realm, username, password):
        if username in self.config.get("users"):
            if self.config.get("users")[username] == password:
                return True

        return False

    def __checkAdminCredentials(self, realm, username, password):
        if username in self.config.get("admins"):
            if self.config.get("admins")[username] == password:
                return True

        return False

    def __getCurrentSession(self):
        return self.sessionHandler.get(self.__getClientIp())

    def __setForCurrentSession(self, attr, val):
        self.sessionHandler.setAttribute(self.__getClientIp(), attr, val)

    def __getForCurrentSession(self, attr):
        return self.__getCurrentSession().get(attr)

    def __returnToLastPage(self):
        if self.__getCurrentSession().exists('lastpage') \
           and self.__getCurrentSession().exists('lastpage'):

            if self.__getCurrentSession().get('lastpageArgs'):
                return \
                    self.__getCurrentSession().get("lastpage")(
                        *self.__getCurrentSession().get('lastpageArgs')
                        )
            else:
                return self.__getCurrentSession().get("lastpage")()

        return self.index()

    def __getClientIp(self):
        return cherrypy.request.headers['Remote-Addr']

    def __refreshSession(self):
        self.sessionHandler.activity(self.__getClientIp())

    def __setLastPage(self, page, args):
        self.sessionHandler.setAttribute(self.__getClientIp(), "lastpage", page)
        self.sessionHandler.setAttribute(
            self.__getClientIp(),
            "lastpageArgs",
            args
            )

    @cherrypy.expose
    def index(self):
        self.__refreshSession()
        return self.artists()

    @cherrypy.expose
    def artists(self):
        self.__refreshSession()
        self.__setLastPage(self.artists, None)
        return self.HTMLBuilder.buildArtistsPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
        )

    @cherrypy.expose
    def artist(self, artist=None):
        self.__refreshSession()
        self.__setLastPage(self.artist, [artist])

        return self.HTMLBuilder.buildArtistPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary,
            artist
        )

    @cherrypy.expose
    def albums(self):
        self.__refreshSession()
        self.__setLastPage(self.albums, None)

        return self.HTMLBuilder.buildAlbumsPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
        )

    @cherrypy.expose
    def album(self, artist=None, album=None):
        self.__refreshSession()
        self.__setLastPage(self.album, [artist, album])

        return self.HTMLBuilder.buildAlbumPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary,
            artist,
            album
        )

    @cherrypy.expose
    def tracks(self):
        self.__refreshSession()
        self.__setLastPage(self.tracks, None)

        return self.HTMLBuilder.buildTracksPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
        )

    @cherrypy.expose
    def track(self, artist=None, album=None, track=None):
        self.__refreshSession()
        self.__setLastPage(self.track, [artist, album, track])

    @cherrypy.expose
    def add(self):
        self.__refreshSession()
        self.__setLastPage(self.add, None)

        return self.HTMLBuilder.buildAddPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary.trackFactory
        )

    @cherrypy.expose
    def addByType(self, trackType=None):
        self.__refreshSession()
        uploadHandler = self.musicLibrary\
                            .trackFactory\
                            .availableTrackTypes[trackType]\
                            .uploadHandler

        self.__setForCurrentSession(
            'uploadHandler',
            uploadHandler(self.config.get("musicDirectory"))
            )

        return self.HTMLBuilder.buildUploadPage(
            self.voteHandler,
            self.playbackQueue,
            uploadHandler.getUploadAttributes()
        )

    @cherrypy.expose
    def upload(self, **args):
        self.__refreshSession()

        trackToAdd = self.__getForCurrentSession('uploadHandler')\
            .trackFromUploadedAttributes(args)

        self.musicLibrary.addArtist(trackToAdd.artistName)
        self.musicLibrary.addAlbum(
            Album.Album(trackToAdd.albumTitle, trackToAdd.artistName)
        )
        self.musicLibrary.addTrack(trackToAdd)

        return self.artist(trackToAdd.artistName)

    @cherrypy.expose
    def startPlaying(self):
        self.__refreshSession()
        self.playbackQueue.startPlaying()
        return self.__returnToLastPage()

    @cherrypy.expose
    def stopPlaying(self):
        self.__refreshSession()
        self.playbackQueue.stopPlaying(True)
        return self.__returnToLastPage()

    @cherrypy.expose
    def voteSkip(self):
        self.__refreshSession()
        self.voteHandler.vote(self.__getClientIp())
        return self.__returnToLastPage()

    @cherrypy.expose
    def addToQueue(self, artist=None, album=None, track=None):
        self.__refreshSession()
        theTrack = self.musicLibrary.artists[
            artist].albums[album].tracks[track]
        self.playbackQueue.addToQueue(theTrack)
        return self.__returnToLastPage()

    @cherrypy.expose
    def addAlbumToQueue(self, artist=None, album=None):
        self.__refreshSession()
        for trackName in self.musicLibrary\
                .artists[artist].albums[album].tracks.keys():

            self.addToQueue(artist, album, trackName)
        return self.__returnToLastPage()

    @cherrypy.expose
    def queue(self):
        self.__refreshSession()
        self.__setLastPage(self.queue, None)

        return self.HTMLBuilder.buildQueuePage(
            self.voteHandler,
            self.playbackQueue
        )

    @cherrypy.expose
    def removeFromQueue(self, artist=None, album=None, track=None):
        self.__refreshSession()
        track = self.musicLibrary.artists[artist].albums[album].tracks[track]
        self.playbackQueue.removeFromQueueByTrack(track)
        return self.__returnToLastPage()

    @cherrypy.expose
    def deleteTrack(self, track=None, artist=None, album=None):
        self.__refreshSession()
        theTrack = self.musicLibrary.artists[
            artist].albums[album].tracks[track]
        self.musicLibrary.deleteTrack(theTrack)
        return self.__returnToLastPage()

    @cherrypy.expose
    def deleteAlbum(self, artist=None, album=None):
        self.__refreshSession()
        theAlbum = self.musicLibrary.artists[artist].albums[album]
        self.musicLibrary.deleteAlbum(theAlbum)
        return self.__returnToLastPage()

    @cherrypy.expose
    def deleteArtist(self, artist=None,):
        self.__refreshSession()
        theArtist = self.musicLibrary.artists[artist]
        self.musicLibrary.deleteArtist(theArtist)
        return self.__returnToLastPage()

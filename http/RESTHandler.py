import os

import cherrypy

import HTMLBuilder
from http import SessionHandler, FloodProtection, VoteHandler


def htmlRelPath(config, path):
    return os.path.join(config.get("htmlDir"), path)


class RESTHandler(object):

    def __init__(self, config, playbackQueue, musicLibrary, trackFactory):
        self.config = config
        self.playbackQueue = playbackQueue
        self.musicLibrary = musicLibrary
        self.trackFactory = trackFactory
        self.sessionHandler = SessionHandler.SessionHandler(self.config)
        self.voteHandler = VoteHandler.VoteHandler(
            self.config,
            self.sessionHandler,
            self.playbackQueue.playNext
        )
        self.floodProtection = FloodProtection.FloodProtection(
            self.config,
            self.sessionHandler
        )

        self.HTMLBuilder = HTMLBuilder.HTMLBuilder(
            config.get("htmlDir"),
            self.floodProtection,
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
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

            "/stopPlaying": {
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

        self.playbackQueue.onFinishedCallback = self.voteHandler.newVoting
        self.playbackQueue.onStoppedCallback = self.voteHandler.newVoting

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

            print(
                "Returning to:",
                self.__getCurrentSession().get('lastpage'))

            if self.__getCurrentSession().get('lastpageArgs'):
                print("with args:", self.__getCurrentSession().get('lastpageArgs'))
                return \
                    self.__getCurrentSession().get("lastpage")(
                        self,
                        **self.__getCurrentSession().get('lastpageArgs')
                    )
            else:
                return self.__getCurrentSession().get("lastpage")()

        return self.index()

    def __getClientIp(self):
        return cherrypy.request.headers['Remote-Addr']

    def __refreshSession(self):
        self.sessionHandler.activity(self.__getClientIp())

    def __setLastPage(self, page, args):
        self.sessionHandler.setAttribute(
            self.__getClientIp(), "lastpage", page)
        self.sessionHandler.setAttribute(
            self.__getClientIp(),
            "lastpageArgs",
            args
        )

    def hasSession(func):
        def wrapper(self, **kwargs):
            self.__refreshSession()
            return func(self, **kwargs)
        return wrapper

    def isReturnable(func):
        def wrapper(self, **kwargs):
            self.__setLastPage(func, kwargs)
            return func(self, **kwargs)
        return wrapper

    def returnsToLast(func):
        def wrapper(self, **kwargs):
            func(self, **kwargs)
            return self.__returnToLastPage()
        return wrapper

    def floodProtected(func):
        def wrapper(self, **kwargs):
            if not self.floodProtection.actionPermitted(self.__getClientIp()):
                return self.__returnToLastPage()
            self.floodProtection.action(self.__getClientIp())
            return func(self, **kwargs)
        return wrapper

    @cherrypy.expose
    @hasSession
    @isReturnable
    def index(self):
        return self.artists()

    @cherrypy.expose
    @hasSession
    @isReturnable
    def artists(self):
        return self.HTMLBuilder.buildArtistsPage(self.__getClientIp())

    @cherrypy.expose
    @hasSession
    @isReturnable
    def artist(self, artist=None):
        return self.HTMLBuilder.buildArtistPage(self.__getClientIp(), artist)

    @cherrypy.expose
    @hasSession
    @isReturnable
    def albums(self):
        return self.HTMLBuilder.buildAlbumsPage(self.__getClientIp())

    @cherrypy.expose
    @hasSession
    @isReturnable
    def album(self, artist=None, album=None):
        return self.HTMLBuilder.buildAlbumPage(
            self.__getClientIp(), artist, album
            )

    @cherrypy.expose
    @hasSession
    @isReturnable
    def tracks(self):
        return self.HTMLBuilder.buildTracksPage(self.__getClientIp())

    @cherrypy.expose
    @hasSession
    @isReturnable
    def track(self, artist=None, album=None, track=None):
        pass

    @cherrypy.expose
    @hasSession
    @isReturnable
    def add(self):
        return self.HTMLBuilder.buildAddPage(self.__getClientIp())

    @cherrypy.expose
    @hasSession
    def addByType(self, trackType=None):
        uploadHandler = self.musicLibrary\
                            .trackFactory\
                            .availableTrackTypes[trackType]\
                            .uploadHandler(self.config.get("musicDirectory"))

        self.__setForCurrentSession(
            'uploadHandler',
            uploadHandler
        )

        return self.HTMLBuilder.buildUploadPage(
            self.__getClientIp(),
            uploadHandler.getUploadAttributes()
        )

    @cherrypy.expose
    @hasSession
    def upload(self, **args):
        trackToAdd = self.__getForCurrentSession('uploadHandler')\
            .trackFromUploadedAttributes(args)
        self.musicLibrary.addTrack(trackToAdd)
        return self.artist(trackToAdd.artistName)

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def startPlaying(self):
        self.playbackQueue.startPlaying()

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def stopPlaying(self):
        self.playbackQueue.stopPlaying(True)

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def voteSkip(self):
        self.voteHandler.vote(self.__getClientIp())

    @cherrypy.expose
    @hasSession
    @floodProtected
    @returnsToLast
    def addToQueue(self, artist=None, album=None, track: str=None):
        theTrack = self.musicLibrary.entries[artist][album][track]
        self.playbackQueue.addToQueue(theTrack)

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def addAlbumToQueue(self, artist=None, album=None):
        for trackName in self.musicLibrary\
                .entries[artist][album].keys():
            self.addToQueue(artist=artist, album=album, track=trackName)

    @cherrypy.expose
    @hasSession
    @isReturnable
    def queue(self):
        return self.HTMLBuilder.buildQueuePage(self.__getClientIp())

    @cherrypy.expose
    @returnsToLast
    def removeFromQueue(self, artist=None, album=None, track: str=None):
        track = self.musicLibrary.entries[artist][album][track]
        self.playbackQueue.removeFromQueueByTrack(track)

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def deleteTrack(self, track=None, artist=None, album=None):
        theTrack = self.musicLibrary.artists[
            artist].albums[album].tracks[track]
        self.musicLibrary.deleteTrack(theTrack)

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def deleteAlbum(self, artist=None, album=None):
        theAlbum = self.musicLibrary.artists[artist].albums[album]
        self.musicLibrary.deleteAlbum(theAlbum)

    @cherrypy.expose
    @hasSession
    @returnsToLast
    def deleteArtist(self, artist=None,):
        theArtist = self.musicLibrary.artists[artist]
        self.musicLibrary.deleteArtist(theArtist)

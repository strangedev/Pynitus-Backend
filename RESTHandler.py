import signal

import cherrypy
from cherrypy.lib import auth_basic

import MusicLibrary
import TrackFactory
import PlaybackQueue
import HTMLBuilder
import VoteHandler
import Album

"""
UARGH
"""
userAndPass = {
    "THEUSER": "THEPASSWD",
    }

adminUserAndPass = {
    "THEADMINNAME": "THEADMINPASSWD"
}


def checkCredentials(realm, username, password):
    if username in userAndPass:
        if userAndPass[username] == password:
            return True

    return False


def checkAdminCredentials(realm, username, password):
    if username in adminUserAndPass:
        if adminUserAndPass[username] == password:
            return True

    return False

cherrypyConf = {
    "/": {
        "tools.auth_basic.on": True,
        "tools.auth_basic.realm": "PiJukebox",
        "tools.auth_basic.checkpassword": checkCredentials,
        "tools.sessions.on": True
    },

    "/removeFromQueue": {
        "tools.auth_basic.on": True,
        "tools.auth_basic.realm": "localhost",
        "tools.auth_basic.checkpassword": checkAdminCredentials,
        "tools.sessions.on": True
    },

    "/deleteTrack": {
        "tools.auth_basic.on": True,
        "tools.auth_basic.realm": "localhost",
        "tools.auth_basic.checkpassword": checkAdminCredentials,
        "tools.sessions.on": True
    },

    "/deleteAlbum": {
        "tools.auth_basic.on": True,
        "tools.auth_basic.realm": "localhost",
        "tools.auth_basic.checkpassword": checkAdminCredentials,
        "tools.sessions.on": True
    },

    "/deleteArtist": {
        "tools.auth_basic.on": True,
        "tools.auth_basic.realm": "localhost",
        "tools.auth_basic.checkpassword": checkAdminCredentials,
        "tools.sessions.on": True
    },

    "/css/bootstrap.min.css": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "THEWDIR/css/bootstrap.min.css"
    },

    "/fonts/glyphicons-halflings-regular.eot": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "THEWDIR/fonts/glyphicons-halflings-regular.eot"
    },

    "/fonts/glyphicons-halflings-regular.svg": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "THEWDIR/fonts/glyphicons-halflings-regular.svg"
    },

    "/fonts/glyphicons-halflings-regular.ttf": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "THEWDIR/fonts/glyphicons-halflings-regular.ttf"
    },

    "/fonts/glyphicons-halflings-regular.woff": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "THEWDIR/fonts/glyphicons-halflings-regular.woff"
    },

    "/fonts/glyphicons-halflings-regular.woff2": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": "THEWDIR/fonts/glyphicons-halflings-regular.woff2"
    },

    '/favicon.ico':
        {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': 'THEWDIR/img/pynitus_32x32.ico'
        },

    '/favicon.png':
        {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': 'THEWDIR/img/pynitus_32x32.png'
        }

}

cherrypy.config.update({'server.socket_port': THEPORT,
                        'log.access_file': './access.log',
                        'log.error_file': './error.log',
                        'server.socket_host': 'THEIPADDR'
                        })


class RESTHandler(object):

    def __init__(self, playbackQueue, musicLibrary, trackFactory):
        self.playbackQueue = playbackQueue
        self.musicLibrary = musicLibrary
        self.trackFactory = trackFactory
        self.HTMLBuilder = HTMLBuilder.HTMLBuilder(
                "THEWDIR/html"
                )
        self.voteHandler = VoteHandler.VoteHandler(self.playbackQueue.playNext)

    @cherrypy.expose
    def index(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        return self.artists()

    @cherrypy.expose
    def artists(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        return self.HTMLBuilder.buildArtistsPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
            )

    @cherrypy.expose
    def artist(self, artist=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.artist
        cherrypy.session['lastpageArgs'] = [artist]
        return self.HTMLBuilder.buildArtistPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary,
            artist
            )

    @cherrypy.expose
    def albums(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.albums
        cherrypy.session['lastpageArgs'] = None
        return self.HTMLBuilder.buildAlbumsPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
            )

    @cherrypy.expose
    def album(self, artist=None, album=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.album
        cherrypy.session['lastpageArgs'] = [artist, album]
        return self.HTMLBuilder.buildAlbumPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary,
            artist,
            album
            )

    @cherrypy.expose
    def tracks(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.tracks
        cherrypy.session['lastpageArgs'] = None
        return self.HTMLBuilder.buildTracksPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary
            )

    @cherrypy.expose
    def track(self, artist=None, album=None, track=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.track
        cherrypy.session['lastpageArgs'] = [artist, album, track]

    @cherrypy.expose
    def add(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.add
        cherrypy.session['lastpageArgs'] = None
        return self.HTMLBuilder.buildAddPage(
            self.voteHandler,
            self.playbackQueue,
            self.musicLibrary.trackFactory
            )

    @cherrypy.expose
    def addByType(self, trackType=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        uploadHandler = self.musicLibrary\
                            .trackFactory\
                            .availableTrackTypes[trackType]\
                            .uploadHandler

        cherrypy.session['uploadHandler'] = uploadHandler("THEMDIR")

        return self.HTMLBuilder.buildUploadPage(
            self.voteHandler,
            self.playbackQueue,
            cherrypy.session['uploadHandler'].getUploadAttributes()
            )

    @cherrypy.expose
    def upload(self, **args):
        self.voteHandler.userActivity(cherrypy.session.id)
        trackToAdd = cherrypy.session['uploadHandler'].trackFromUploadedAttributes(args)
        self.musicLibrary.addArtist(trackToAdd.artistName)
        self.musicLibrary.addAlbum(
            Album.Album(trackToAdd.albumTitle, trackToAdd.artistName)
            )
        self.musicLibrary.addTrack(trackToAdd)
        return self.artist(trackToAdd.artistName)#self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def startPlaying(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        self.playbackQueue.startPlaying()
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def stopPlaying(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        self.playbackQueue.stopPlaying(True)
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def voteSkip(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        self.voteHandler.vote(cherrypy.session.id)
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def addToQueue(self, artist=None, album=None, track=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        print("Adding tq: ", artist, album, track)
        theTrack = self.musicLibrary.artists[artist].albums[album].tracks[track]
        self.playbackQueue.addToQueue(theTrack)
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def queue(self):
        self.voteHandler.userActivity(cherrypy.session.id)
        cherrypy.session['lastPage'] = self.queue
        cherrypy.session['lastpageArgs'] = None
        return self.HTMLBuilder.buildQueuePage(
            self.voteHandler, 
            self.playbackQueue
            )

    @cherrypy.expose
    def removeFromQueue(self, artist=None, album=None, track=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        track = self.musicLibrary.artists[artist].albums[album].tracks[track]
        self.playbackQueue.removeFromQueueByTrack(track)
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def deleteTrack(self, track=None, artist=None, album=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        theTrack = self.musicLibrary.artists[artist].albums[album].tracks[track]
        self.musicLibrary.deleteTrack(theTrack)
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def deleteAlbum(self, artist=None, album=None):
        self.voteHandler.userActivity(cherrypy.session.id)
        theAlbum = self.musicLibrary.artists[artist].albums[album]
        self.musicLibrary.deleteAlbum(theAlbum)
        return self.returnToLastPage(cherrypy.session)

    @cherrypy.expose
    def deleteArtist(self, artist=None,):
        self.voteHandler.userActivity(cherrypy.session.id)
        theArtist = self.musicLibrary.artists[artist]
        self.musicLibrary.deleteArtist(theArtist)
        return self.returnToLastPage(cherrypy.session)

    def returnToLastPage(self, userSession):
        if 'lastPage' in cherrypy.session and 'lastpageArgs' in cherrypy.session:

            if cherrypy.session['lastpageArgs']:
                return cherrypy.session['lastPage'](*cherrypy.session['lastpageArgs'])
            else:
                return cherrypy.session['lastPage']()

        return self.index()

musicLibrary = MusicLibrary.MusicLibrary("THEMDIR")
playbackQueue = PlaybackQueue.PlaybackQueue()
trackFactory = TrackFactory.TrackFactory()

cherrypy.quickstart(
    RESTHandler(playbackQueue, musicLibrary, trackFactory),
    "/",
    cherrypyConf
    )

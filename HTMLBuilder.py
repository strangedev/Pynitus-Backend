#from xml.etree import ElementTree
import os

import jinja2

class HTMLBuilder(object):

	def __init__(self, templatePath):

		self.templatePath = templatePath

		self.environment = jinja2.Environment(
			loader=jinja2.FileSystemLoader(self.templatePath)
    		)

	def buildArtistsPage(self, voteHandler, playbackQueue, musicLibrary):

		template = self.environment.get_template("artists.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			artistNames = sorted([artist.name for artist in musicLibrary.getArtists()])
			)

	def buildAlbumsPage(self, voteHandler, playbackQueue, musicLibrary):
		
		template = self.environment.get_template("albums.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			albumAndArtistNames = sorted([(album.title, album.artistName) for album in musicLibrary.getAlbums()])
			)

	def buildTracksPage(self, voteHandler, playbackQueue, musicLibrary):
		
		template = self.environment.get_template("tracks.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			trackAndAlbumAndArtistNames = sorted([(track.title, track.albumTitle, track.artistName) for track in musicLibrary.getTracks()])
			)

	def buildQueuePage(self, voteHandler, playbackQueue):
		
		template = self.environment.get_template("queue.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			trackAndAlbumAndArtistNames = [(track.title, track.albumTitle, track.artistName) for track in playbackQueue.getQueued()]
			)

	def buildArtistPage(self, voteHandler, playbackQueue, musicLibrary, artist):
		
		template = self.environment.get_template("artist.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			albumTitles = sorted([album.title for album in musicLibrary.getAlbumsForArtist(artist)]),
			trackAndAlbumTitles = sorted([(track.title, track.albumTitle) for track in musicLibrary.getTracksForArtist(artist)]),
			artistName = artist
			)


	def buildAlbumPage(self, voteHandler, playbackQueue, musicLibrary, artist, album):
		
		template = self.environment.get_template("album.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			albumTitle = album,
			artistName = artist,
			trackTitles = sorted([track.title for track in musicLibrary.getTracksForAlbumOfArtist(artist, album)])
			)

	def buildTrackPage(self, voteHandler, playbackQueue, track):
		pass

	def buildAddPage(self, voteHandler, playbackQueue, trackfactory):
		
		template = self.environment.get_template("add.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			trackTypesAndDescs = sorted([(trackType, trackfactory.availableTrackTypes[trackType].description) for trackType in trackfactory.availableTrackTypes])
			)

	def buildUploadPage(self, voteHandler, playbackQueue, attributes):
		
		template = self.environment.get_template("upload.html")

		return template.render(
			playbackQueue = playbackQueue,
			voteCount = voteHandler.votes,
			votesRequired = voteHandler.getRequiredVotes(),
			playing = playbackQueue.playing,
			attributes = attributes
			)
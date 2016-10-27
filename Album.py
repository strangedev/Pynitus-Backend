import Track

class Album(object):
	"""
	Superclass
	"""

	def __init__(
		self, 
		title, 
		artistName, 
		features=None,
		releaseDate = None,
		genre = None
		):
		
		self.title = title
		self.artistName = artistName
		self.features = features if features else []
		self.releaseDate = releaseDate
		self.genre = genre
		self.tracks = dict({})

	def addTrack(self, track):

		self.tracks[track.title] = track

	def getTracks(self):

		return list(self.tracks.values())
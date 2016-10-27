import Album

class Artist(object):

	def __init__(self, name):
		
		self.name = name
		self.albums = dict({})

	def addAlbum(self, album):

		#print("Album exists: ", album.title, " => ", album.title in self.albums)
		#print("Known albums: ", self.albums)

		if not album.title in self.albums:
			self.albums[album.title] = album

	def getAlbums(self):

		return list(self.albums.values())
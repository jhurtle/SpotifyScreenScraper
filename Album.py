import copy
import Song

class Album:
	artist = []
	imageLarge = ""
	imageSmall = ""
	tracks = []
	name = ""
	releaseDate = ""
	
	def setArtists(self,artist):
		self.artist = copy.deepcopy(artist)
	def getArtist(self):
		return copy.deepcopy(self.artist)
	def setImageLarge(self,imageLarge):
		self.imageLarge = imageLarge
	def getImageLarge(self):
		return self.imageLarge
	def setImageSmall(self,imageSmall):
		self.imageSmall = imageSmall
	def getImageSmall(self):
		return imageSmall
	def setTracks(self,tracks):
		self.tracks = copy.deepcopy(tracks)
	def getTracks(self):
		return copy.deepcopy(self.tracks)
	def setName(self,name):
		self.name = name
	def getName(self):
		return self.name
	def setReleaseDate(self,releaseDate):
		self.releaseDate = releaseDate
	def getReleaseDate(self):
		return self.releaseDate
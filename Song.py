import copy

class Song:
	name = ""
	artists = []
	duration = 0
	explicit = 0
	lyrics = ""
	trackNum = 0
	def __init__(self):
		self.name = ""
	def setName(self,name):
		self.name = name
	def getName(self):
		return self.name
	def setArtists(self,artists):
		self.artist = copy.deepcopy(artists)
	def getArtists(self):
		return copy.deepcopy(self.artists)
	def setDuration(self,duration):
		self.duration = duration
	def getDuration(self):
		return self.duration
	def setExplicit(self,explicit):
		self.explicit = explicit
	def getExplicit(self):
		return self.explicit
	def setLyrics(self,lyrics):
		self.lyrics = lyrics
	def getLyrics(self):
		return self.lyrics
	def setTrackNum(self,trackNum):
		self.trackNum = trackNum
	def getTrackNum(self):
		return self.trackNum
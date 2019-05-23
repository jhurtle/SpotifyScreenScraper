import copy
import Album

class Artist:
	followers = 0
	genres = []
	name = ""
	imageLarge = ""
	imageMed = ""
	imageSmall = ""
	albumList = []
	bio = ""
	
	def setFollowers(self,followers):
		self.followers = followers
	def getFollowers(self):
		return self.followers
	def setGenres(self,genres):
		self.genres = copy.deepcopy(genres)
	def getGenres(self):
		return copy.deepcopy(self.genres)
	def setName(self,name):
		self.name = name
	def getName(self):
		return self.name
	def setImageLarge(self,imageLarge):
		self.imageLarge = imageLarge
	def getImageLarge(self):
		return self.imageLarge
	def setImageMed(self,imageMed):
		self.imageMed = imageMed
	def getImageMed(self):
		return self.imageMed
	def setImageSmall(self,imageSmall):
		self.imageSmall = imageSmall
	def getImageSmall(self):
		return self.imageSmall
	def setAlbumList(self,albumList):
		self.albumList = copy.deepcopy(albumList)
	def getAlbumList(self):
		return copy.deepcopy(self.albumList)
	def setBio(self,bio):
		self.bio = bio
	def getBio(self):
		return self.bio
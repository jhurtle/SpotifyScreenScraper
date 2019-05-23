import pylast

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "0b027fa9f622b479fdd798b727639803"  # this is a sample key
API_SECRET = "5fdf4afa085493609fa010d3d99cd8c4"

username = "jjhurtle"
password_hash = pylast.md5("Icbm#3037")

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash)
	
def get_artist_bio(artistName):
	artist = pylast.Artist(artistName,network)
	return artist.get_bio_content()
	
def get_album_release(artistName,albumName):
	album = network.get_album(artistName,albumName)
	try:
		return album.get_wiki_published_date().split(",")[0]
	except Exception:
		return None

import lastfm_extension.pylast as pylast

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "0b027fa9f622b479fdd798b727639803"  # this is a sample key
API_SECRET = "5fdf4afa085493609fa010d3d99cd8c4"

username = "jjhurtle"
password_hash = pylast.md5("Icbm#3037")

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash)
artist = pylast.Artist("Drake",network)
print(artist.get_upcoming_events())
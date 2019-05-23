import sys
import spotipy
import spotipy.util as util
import pylyrics3.pylyrics3 as lyrics
import copy
import authorizeSpotify as authorize
from Artist import Artist
from Album import Album
from Song import Song
import urllib.request
import os
import json
import lastfm

sp = None
token = None
hit = 0
miss = 0

def getAuthorization():
	global sp
	global token
	
	if sp is None or authorize.is_token_expired():
		token = authorize.get_access_token(token,client_id,client_secret)
		sp = spotipy.Spotify(auth=token['access_token'])
		
	

def getLyrics(artist,songName,albumName):
	global hit
	global miss
	l = None
	for ch in ['(',')','\'','&']:
		try:
			if(ch in songName and ch is '('):
				firstIndex = songName.index('(')
				secIndex = songName.index(')')
				if(firstIndex != -1 and secIndex != -1):
					songName = songName.replace(
					songName[firstIndex:secIndex+1],"").strip()
			#if(ch in artist and ch is '('):
			#	firstIndex = artist.index('(')
			#	secIndex = artist.index(')')
			#	if(firstIndex != -1 and secIndex!=-1):
			#		artist = artist.replace(
			#		artist[firstIndex:secIndex+1],"").strip()
			if(ch in songName and ch is '\''):
				songName = songName.replace('\'','%27')
			if(ch in songName and ch is '&'):
				songName = songName.replace('&',' %26 ')
			if(ch in artist and ch is '&'):
				artist = artist.replace('&',' %26 ')
			if(ch in artist and ch is '\''):
				artist = artist.replace('\'','%27')
		except Exception as e:
			print("Error: ",e)
	print("-----------------------------------")
	try:
		l = lyrics.get_song_lyrics(artist,songName)
		if(l is not None):
			print("Successfully downloaded-> ","Artist: ",artist,", Album: ",albumName," , Song: ",songName)
			hit = hit + 1
			return l
	except Exception as e:
		print("Error: ",e)
		
	if(l is None):
		if('-' in songName):
			index = songName.index('-')
			songName = songName.replace(songName[index:len(songName)],"")
			try:
				l = lyrics.get_song_lyrics(artist,songName)
				if(l is not None):
					print("\tRecovered downloaded-> ","Artist: ",artist,", Album: ",albumName,", Song: ",songName)
					hit = hit + 1
					return l
			except Exception as e:
				print("Error: ",e)
	if(l is None):
		if('feat' in songName):
			try:
				index = songName.index('feat')
				songName = songName.replace(songName[index:len(songName)],"")
				l = lyrics.get_song_lyrics(artist,songName)
				if(l is not None):
					print("\tRecovered downloaded-> ","Artist: ",artist,", Album: ",albumName,", Song: ",songName)
					hit = hit + 1
					return l
			except Exception as e:
				print("Error: ",e)
	if(l is None):
		print("Fail: ","Artist: ",artist,", Album: ",albumName,", Song: ",songName)
		miss = miss + 1
		return ""
		
def getSongInfo(token_info,artistName,albumName):
	duration_ms = token_info['duration_ms']
	name = token_info['name']
	explicit = token_info['explicit']
	artistList = []
	lyrics = getLyrics(artistName,name,albumName)
	for x in token_info['artists']:
		artistList.append(x['name'])
	song = Song()
	song.setName(name)
	song.setDuration(duration_ms)
	song.setExplicit(explicit)
	song.setArtists(artistList)
	song.setLyrics(lyrics)
	song.setTrackNum(token_info['track_number'])
	return song
	
def getAlbumInfo(token_info,songList):
	name = token_info['name']
	artistList = []
	for x in token_info['artists']:
		artistList.append(x['name'])
	imageList = []
	for x in token_info['images']:
		imageList.append(x['url'])
	album = Album()
	if(len(imageList)>=1):
		album.setImageLarge(imageList[0])
	if(len(imageList)>=2):
		album.setImageSmall(imageList[1])
	album.setName(name)
	album.setArtists(artistList)
	album.setTracks(songList)
	return album
	
def getArtistInfo(token_info,albumList):
	name = token_info['name']
	genres = []
	for x in token_info['genres']:
		genres.append(x)
	followers = token_info['followers']['total']
	imageList = []
	for x in token_info['images']:
		imageList.append(x['url'])
	artist = Artist()
	if(len(imageList)>=1):
		artist.setImageLarge(imageList[0])
	if(len(imageList)>=2):
		artist.setImageMed(imageList[1])
	if(len(imageList)>=3):
		artist.setImageSmall(imageList[2])
	artist.setName(name)
	artist.setFollowers(followers)
	artist.setGenres(genres)
	artist.setAlbumList(albumList)
	try:
		artist.setBio(lastfm.get_artist_bio(name))
	except Exception:
		print("Artist Biography content could not be retrieved")
	return artist
	
def getArtistImages(artist,dir):
	artistName = artist.getName()
	largeImageFile = dir + '\\' + artistName+'Large.png'
	medImageFile = dir + '\\' +artistName+ 'Med.png'
	smallImageFile = dir + '\\' +artistName+ 'Small.png'
	urllib.request.urlretrieve(artist.getImageLarge(),largeImageFile)
	urllib.request.urlretrieve(artist.getImageMed(),medImageFile)
	urllib.request.urlretrieve(artist.getImageSmall(),smallImageFile)
	
def getAlbumImages(albumJson,dir):
	album = albumJson
	albumName = album['setName'].replace("/","")
	albumName = albumName.replace('\\','')
	albumName = albumName.replace(" ","")
	albumName = albumName.replace("\"","")
	
	largeImageFile = dir + '\\' + albumName+'Large.png'
	smallImageFile = dir + '\\' +albumName+ 'Small.png'
	urllib.request.urlretrieve(album['imageSmall'],smallImageFile)
	urllib.request.urlretrieve(album['imageLarge'],largeImageFile)
	
def getImages(artist,albumList,dir):
	try:
		getArtistImages(artist,dir)
	except (Exception) as e:
		print("Artist Image Failed to Download: ",e)
	for x in albumList:
		try:
			getAlbumImages(x,dir)
		except (Exception) as e:
			print("Album Image Failed to Download: ",e)
	
	
	

client_id='4c712d6bc65d44f9b2dcf24694754ecc'
client_secret='aed502ac81c84679addf435af1a77916'
redirect_uri='https://example.com/callback/'

scope = 'user-library-read'
username = 'jhurtle'

#token = util.prompt_for_user_token(username, scope,client_id,client_secret,redirect_uri)	
	
def main():
	global sp
	global token
	global hit
	global miss
	songSet =  set()
	albumSet = set()
	genreSet = set()
	artistList = []
	
	cwd = os.getcwd()
	artistDirectory = cwd +'\Artists'
	if not os.path.exists(artistDirectory):
		os.makedirs(artistDirectory)
		print("Artist Directory Created")
	
	
	with open('TopArtists.txt','r') as f:
		for line in f:
			try:
				getAuthorization()
				results = sp.search(q='artist:'+line.strip(), type='artist')
				artistList = results['artists']['items']
				if artistList == []:
					print("No Artists Found By The Name of ",line.strip())
					continue
				artist = artistList[0]
				artistName = artist['name']
				results = sp.artist_albums(artist['id'],album_type='album')
				album = []
				album.extend(results['items'])
				for x in artist['genres']:
					if x not in genreSet:
						genreSet.add(x)
				while results['next']:
					results = sp.next(results)
					album.extend(results['items'])
				albumList = []
				for x in album:
					albumName = x['name']
					album = None
					songList = []
					if albumName not in albumSet:
						albumSet.add(albumName)
						getAuthorization()
						songs = sp.album(x['id'])['tracks']['items']
						for y in songs:
							song = None
							songName = y['name']
							if songName not in songSet:
								songSet.add(songName)
								song = getSongInfo(y,artistName,albumName)
								songList.append(json.loads(json.dumps(vars(song))))
						album = getAlbumInfo(x,songList)
						albumList.append(json.loads(json.dumps(vars(album))))
				artist_info = getArtistInfo(artist,albumList)
				artistList.append(artist_info)
				formatArtistName = artistName.replace(" ","")
				formatArtistName = formatArtistName.replace("\\","")
				formatArtistName = formatArtistName.replace("\"","")
				formatArtistName = formatArtistName.replace("\'","")
				newDir = artistDirectory + '\\' + formatArtistName
				if not os.path.exists(newDir):
					os.makedirs(newDir)
					print(artistName + " Directory Created")
				fileName = newDir +"\\"+formatArtistName + ".txt"
				with open(fileName, 'w') as outFile:
					json.dump(vars(artist_info),outFile)
				getImages(artist_info,albumList,newDir)
			except Exception as e:
				print("Failure in Getting Artist Files: ",e)
			total = hit + miss
			accuracy = (hit/float(total))*100
			print("Total: ",total)
			print("Accuracy : %.2f" % accuracy,"%")
			print("Hit: ",hit)
			print("Miss: ",miss)
		with open("Genres.txt",'w') as genreFile:
			for x in genreSet:
				genreFile.write(x)
main()
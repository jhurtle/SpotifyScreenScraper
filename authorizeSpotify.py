import base64
import requests
import os
import json
import time
import sys
import spotipy
import spotipy.util as util

import six
import six.moves.urllib.parse as urllibparse

OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

expires_at = None

def make_authorization_headers(client_id,client_secret):
	auth_header = base64.b64encode(six.text_type(client_id + ":"+client_secret).encode('ascii'))
	return {'Authorization':'Basic %s' % auth_header.decode('ascii')}

def request_access_token(client_id,client_secret):
	payload = {'grant_type' : 'client_credentials'}
	
	header = make_authorization_headers(client_id,client_secret)
	response = requests.post(OAUTH_TOKEN_URL,data=payload,headers=header,proxies=None)
	
	if response.status_code == 429:
		wait_token = response.json()
		print(wait_token)
		wait_time = wait_token['retry_after'] + 15
		print("Too Many Requests Retry After: ",wait_time)
		time.sleep(wait_time)
		return request_access_token(client_id,client_secret)
	if response.status_code != 200:
		raise SpotifyOauthError(response.reason)

	token_info = response.json()
	return token_info
	
def is_token_expired():
	global expires_at
	now = int(time.time())
	return expires_at - now < 60 * 5
	
def get_access_token(token_info,client_id,client_secret):
	global expires_at
	if token_info and not is_token_expired():
		print("Old Info_Token Returned")
		return token_info
	else:
		print("New Info_Token Created")
		new_token = request_access_token(client_id,client_secret)
		expires_at = new_token['expires_in'] + int(time.time())
		return new_token
		
if __name__=='__main__':
	token1 = request_access_token(client_id,client_secret)
	print(token1['access_token'])
	token2 = get_access_token(token1,client_id,client_secret)
	print(token2['access_token'])
	token3 = request_access_token(client_id,client_secret)
	print(token3['access_token'])
	





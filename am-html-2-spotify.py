"""
Use the HTML from an Apple Music playlist page to create a Spotify playlist

Steps:
	Configure
	Parse HTML
	Create playlist in Spotify
	Search for songs in Spotify
	Add songs to new playlist in Spotify

Author: Blake Johnson

#https://medium.com/@leighmurray_10641/creating-a-spotify-playlist-with-python-7ff7ee94f612
#https://medium.com/analytics-vidhya/build-your-own-playlist-generator-with-spotifys-api-in-python-ceb883938ce4
"""

from bs4 import BeautifulSoup
from html.parser import HTMLParser
import urllib.request
import json
import requests
import re
import configparser

#======================================================================================Configure======================================================================================
config = configparser.ConfigParser()
config.read("config.ini")
playlist_name = config["DEFAULT"]["playlist_name"]
playlist_description = config["DEFAULT"]["playlist_description"]
user_id = config["DEFAULT"]["user_id"]
token = config["DEFAULT"]["token"]
html_file = str(config["DEFAULT"]["html_file"])

#======================================================================================Parse HTML======================================================================================
with urllib.request.urlopen(html_file) as h:
		html = h.read()
parsed_html = BeautifulSoup(html, features="html.parser")
song_name_wrappers = parsed_html.findAll('div', attrs={'class':"song-name-wrapper"})

results = {}
count = 0
for r in song_name_wrappers:
	for div in r.findAll('div'):
		if "song-name" in div.get("class"):
			results[count] = {"song": div.text}
		if "by-line" in div.get("class"):
			if div.span.a:
				results[count]["artist"] = div.span.a.text
			else:
				results[count]["artist"] = div.span.span.text
	count = count + 1

for k, v in results.items():
	v["song"] = v["song"].replace("\n", "")
print("Parse HTML -- results: {}".format(len(results)))

#======================================================================================Create playlist in Spotify======================================================================================
create_endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
create_request_body = json.dumps({
          "name": "{}".format(playlist_name),
          "description": "{}".format(playlist_description),
          "public": False
        })
create_response = requests.post(url = create_endpoint_url, data = create_request_body, headers={"Content-Type":"application/json", "Authorization":"Bearer {}".format(token)})
playlist_id = create_response.json()['id']
print("Create Playlist -- status code: {}".format(create_response.status_code))

#======================================================================================Search for songs in Spotify===========================================y===========================================
uris = []
for v in results.values():
	# Song and Artist name from HTML file
	song_name = v["song"]
	artist_name = v["artist"]
	# Clean up the Song and Artist name for better search results
	song_name = re.sub("[\(\[].*?[\)\]]", "", song_name.lower().strip())
	artist_name = artist_name.lower().strip()

	#Search for song/artist
	next_endpoint = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=50"
	found = False
	while not found and next_endpoint:
		# Query Spotify for songs with song_name
		search_response = requests.get(url = next_endpoint, headers={"Content-Type":"application/json", "Authorization":"Bearer {}".format(token)})

		# If the search was successful, try to match one of the results with the song name and artist from the HTML file
		if search_response.status_code == 200:

			# Check each item and try to match the song name and artist name
			search_dict = search_response.json()
			found = False
			for i in search_dict["tracks"]["items"]:
				sname = i["name"]
				sname = re.sub("[\(\[].*?[\)\]]", "", sname.lower().strip())
				for a in i["artists"]:
					aname = a["name"]
					aname = aname.lower().strip()
					if (song_name in sname or sname in song_name) and (aname in artist_name or artist_name in aname):
						# Found a match, add to uris list and break out of the loop
						uris.append(i["uri"])
						found = True
						break
				if found:
					break

			# If the correct match is not in this response, issue another query with the next_endpoint (found in the current response)
			if not found:
				next_endpoint = search_dict["tracks"]["next"]

		# If the search was not successful, print the song name and artist that was not matched
		else:
			print("Bad Search: song:{} artist:{} code:{}".format(song_name, artist_name, search_response.status_code))
			found = True
			break

	# If there is not a next_endpoint and we did not find the song name, print the song name and artist that was not matched
	if not found:
		print("Not Found: song:{} artist:{}".format(song_name, artist_name))

print("Search for Songs -- results: {}".format(len(uris)))

#======================================================================================Add songs to new playlist======================================================================================
def divide_chunks(l, n):
    for i in range(0, len(l), n):  
        yield l[i:i + n]

sublists = list(divide_chunks(uris, 50))
for l in sublists:
	songs_endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
	songs_request_body = json.dumps({
	          "uris" : l
	        })
	songs_response = requests.post(url = songs_endpoint_url, data = songs_request_body, headers={"Content-Type":"application/json", "Authorization":"Bearer {}".format(token)})
print("Add Songs -- status code: {}".format(songs_response.status_code))
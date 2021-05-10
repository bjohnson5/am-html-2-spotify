# am-html-2-spotify
Use the HTML from an Apple Music playlist page to create a Spotify playlist

Input HTML file
===============
Generate an HTML file by navigating to an Apple Music playlist in a web browser. Use the web inspector to copy all of the HTML on the page and paste it into an .html text file.
The Apple Music playlist page in the browser may not have all the songs listed when you first load the page, javascript is used to load more songs as you scroll down. In order to 
get all the songs on the playlist, scroll all the way down to the bottom of the playlist before copying the HTML.

OAuth Token
===========
In order to issue queries and create/edit playlists you will need a spotify OAuth Token. You can get a temporary one here: https://developer.spotify.com/console/.
Make sure to select the following scopes: playlist-modify-public, playlist-modify-private. This token will expire, so generate a new one right before each run.
This link is also helpful for getting and testing the different endpoint and API calls.

Apple Music API
===============
This all would be much easier if apple let anyone use thier AM api. They have one and that would allow people to query the data rather than scraping an html page. But you have to pay
for the yearly apple developer account in order to get an authentication token to use the api.

User ID
=======
You will also need your spotify user id, to get this share you profile and copy the link. The first string before the "=" is your user id.

Config
======
Set the variables in the "config.ini" file before running. Do not include quotes around the values in the config file.

Requirements
============
- bs4 (BeautifulSoup)
- HTMLParser
- urllib.request
- json
- requests
- re
- configparser

Example:
========
Use this config:
```
[DEFAULT]
playlist_name = Ceej - Pt II
playlist_description = Playlist created by python project: https://github.com/bjohnson5/am-html-2-spotify.git
user_id = <your userid>
token = <your token>
html_file = file:////am-html-2-spotify/ceej-ptii.html
```

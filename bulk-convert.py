from csv import reader
from selenium import webdriver
import sys
import subprocess

class Playlist:
    def __init__(self, name, url, id) -> None:
        self.name = name
        self.url = url
        self.id = id
        self.html_file = ""

    def set_html_file(self, html_file):
        self.html_file = html_file

# Get the token, userid, and prefix
user_id = sys.argv[1]
token = sys.argv[2]
prefix = sys.argv[3]

# Read the links.txt file and parse the link and playlist name
playlist_list = []
count = 0
with open("links.csv", "r") as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        p = Playlist(row[0], row[1], count)
        playlist_list.append(p)
        count = count + 1

# Save the html file for all playlists
subprocess.run(["mkdir", "html/"+prefix], stdout=subprocess.PIPE)
browser = webdriver.Firefox()
for p in playlist_list:
    p.set_html_file("html/"+prefix+"/"+prefix+"p"+str(p.id)+".html")
    browser.get(p.url)
    input("Scroll down the page to load all songs. Then press Enter to continue...")
    html = browser.page_source
    html_file = open(p.html_file, "w")
    html_file.write(html)
    html_file.close()
browser.close()

# Write the config file and run am-html-2-spotify for each playlist
for p in playlist_list:
    config_str = "[DEFAULT]\nplaylist_name = "+p.name+"\nplaylist_description = Playlist created by python project: https://github.com/bjohnson5/am-html-2-spotify.git\nuser_id = "+user_id+"\ntoken = "+token+"\nhtml_file = file:////home/blake/Dropbox/Software Projects/am-html-2-spotify/"+p.html_file
    config_file = open("config.ini", "w")
    config_file.write(config_str)
    config_file.close()
    result = subprocess.run(["python3", "am-html-2-spotify.py"], stdout=subprocess.PIPE)
    print(result.stdout.decode("utf-8"))

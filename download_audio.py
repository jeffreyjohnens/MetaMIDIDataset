import os
import time
import requests
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def download(url, path):
  with open(path, "wb") as f:
    f.write( requests.get(url).content )

chunk = 50
path = "path/to/MMD_audio_matches.tsv"
client_id = "your_spotify_api_client_id"
client_secret = "your_spotify_api_client_secret"
mp3_folder = "save_mp3s_here"

# make folder if necessary
os.makedirs(mp3_folder, exist_ok=True)

# get a list of matched unique spotify ids
spotify_ids = list(pd.unique(pd.read_csv(path, delimiter="\t")["sid"]))

# initialize spotipy
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# download all mp3s
for i in range(0,len(spotify_ids),chunk):
  spotify_id_chunk = spotify_ids[i:i+chunk]
  print(spotify_id_chunk)
  for track in spotify.tracks(spotify_id_chunk)["tracks"]:
    try:
      path = os.path.join(mp3_folder,track["id"]+".mp3")
      download( track["preview_url"], path )
    except Exception as e:
      print(e)
    time.sleep(1) # be nice to the servers
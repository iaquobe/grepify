import sys
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify_api_dir = "./api/spotify/"

def get_credentials(dir_path):
    with open(dir_path + "client-id", "r") as id_file, \
         open(dir_path + "client-secret", "r") as secret_file:
             return id_file.readline(),secret_file.readline()


# initializing api
sci, scs = get_credentials(spotify_api_dir)
credentials = SpotifyClientCredentials(client_id=sci, client_secret=scs)
sp = spotipy.Spotify(client_credentials_manager=credentials)


def print_tracks(tracks):
    def print_ctracks(ctracks):
        for i, item in enumerate(ctracks['items']):
            track = item['track']
            print("%s %s" % (track['artists'][0]['name'], track['name']))

    print_ctracks(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        print_ctracks(tracks)



tracks = sp.playlist_tracks(sys.argv[-1])
print_tracks(tracks)


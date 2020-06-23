import sys
import os
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import lyricsgenius

api_dir = "./api/"
lyrics_dir = "./lyrics/"

def get_credentials():
    with open(api_dir + "spotify/client-id", "r") as id_file, \
         open(api_dir + "spotify/client-secret", "r") as secret_file, \
         open(api_dir + "genius/client-access-token", "r") as token_file:
             return id_file.readline(),secret_file.readline(),token_file.readline()


# initializing api
sci, scs, gct= get_credentials()

#spotify api
credentials = SpotifyClientCredentials(client_id=sci, client_secret=scs)
sp = spotipy.Spotify(client_credentials_manager=credentials)

#genius api
gn = lyricsgenius.Genius(gct)
gn.verbose=False


def get_tracks(tracks):
    def get_ctracks(ctracks, res):
        for i, item in enumerate(ctracks['items']):
            track = item['track']
            artist = track['artists'][0]['name']
            track_name = track['name']

            if artist not in res:
                res[artist] = set()
            res[artist].add(track_name)
        return res

    res = dict()
    res = get_ctracks(tracks, res)
    while tracks['next']:
        tracks = sp.next(tracks)
        res = get_ctracks(tracks, res)
    return res 


def save_lyrics(tracks, playlist_dir):
    for artist_name, songs in tracks.items():
        #create artist dir if not existing
        clean_artist_name = re.sub("[^A-Za-z0-9]+","","%s" % (artist_name))
        if not os.path.isdir(playlist_dir + clean_artist_name):
            os.mkdir(playlist_dir + clean_artist_name)

        for song_name in songs:
            #create song file if it does not exist
            clean_song_name = re.sub("[^A-Za-z0-9_]+","",song_name)
            song_path = playlist_dir + clean_artist_name + "/" + clean_song_name
            if not os.path.exists(song_path):
                with open(song_path, "w+") as out_file:
                    song = gn.search_song(song_name, artist_name)
                    if song is not None :
                        out_file.write("%s, %s:i\n" % (artist_name, song_name))
                        out_file.write(song.lyrics)
                    


#create directories if they dont exist
if not os.path.isdir(lyrics_dir):
    os.mkdir(lyrics_dir)

playlist_id = sys.argv[-1] 


playlist = sp.playlist(playlist_id)

playlist_dir = lyrics_dir + re.sub("[^A-Za-z0-9_]+","",playlist['name']) + "/"
print(playlist_dir)
if not os.path.isdir(playlist_dir):
    os.mkdir(playlist_dir)


tracks = get_tracks(playlist['tracks'])
save_lyrics(tracks, playlist_dir)


# for artist_name, track_list in tracks.items():
#    for track in track_list:
#       print("%s , %s" % (artist_name,track))

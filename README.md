# Introduction

It's grep for lyrics in a Spotify playlist.\
Because there is no better way to search things than with a regex.

# Usage

Right now `spotigrep` is just a proof of concept, here are the limitations that come with it:\
* there is no installation
* the genius api is downloading at painfully slow speed (I'll look into that soon)
* you need to run it from the git root (the file references need it that way)

## Setup

### API keys

first you need api keys for `Spotify` and `Genius`

You can get both for free at:\
https://developer.spotify.com/documentation/web-api/\
under Dashboard\
and:\
https://docs.genius.com/
under Manage Clients\

now save the the keys in `./api/spotify/client-id`, 
`./api/spotify/client-secret`, and `./api/genius/client-access-token`

### Storing the lyrics

By default the lyrics are stored in `./lyrics/`.\
If you want it another way change `api_dir` in spotygrep.py

the lyrics folder is structured as follows:\
`./lyrics/PLAYLIST/ARTIST/SONG`\

## Getting started

For now spotifgrep only downloads lyrics into the aformentioned file structure.\
The only way to use is running:\
`python spotigrep.py [PLAYLIST_ID]`\
The `playlist_id` is the last string in the webplayer when you have the playlist open.

depending on the size of the playlist it could take a couple of minutes.\
I ran it on a Playlist with approx. 100 songs and it took about 5-10min. (again: I'll be trying to improve the time)\

If you are as unpatient as I am you can repeatedly run: `ls lyrics/PLAYLIST/*/* | wc -l` to check how many lyrics you've downloaded.\
Note that all names (playlist, artist, song) are stripped of any characters that fit: `[^A-Za-z0-9]`\

Once you finished downloading the lyrics you can simply run:\
`grep ... lyrics/PLAYLIST/*/*`\

# TODO

* installation so that it can be run from any dir
* shell wraper so the usage mirrors `grep`
* shorten genius download time

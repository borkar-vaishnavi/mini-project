import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch

PLAYLISTS = [['Top Hindi', 'https://open.spotify.com/playlist/37i9dQZF1DX0XUfTFmNBRM', "PL59eqqQABruMQOPlUVcVsIid685ZdwDjf"],
             ['Romantic', 'https://open.spotify.com/playlist/2l4kI8wDwl5F2IT2kjgV7sc',
                 "PL59eqqQABruMSx6VSy1hbkBhG4XwtgSuy"],
             ['Party', 'https://open.spotify.com/playlist/54eevRE0I1lDL0KZwd0X8R',
                 'PL59eqqQABruN3GyAPiPnQ6Jq-TngWjT-Y'],
             ['Top English', 'https://open.spotify.com/album/1ZAQV2h2SZgEiO7UT0xTzg',
              'PL59eqqQABruNew5O0cRvomfbU6FI0RGyl'],
             ['Arijit Singh', 'https://open.spotify.com/playlist/37i9dQZF1DWYztMONFqfvX',
              'PL59eqqQABruM3TLAGthvgW10c1R6omGwq']
             ]
client_credentials_manager = SpotifyClientCredentials(client_id='fd63f6cdd7b34c4e8fbd7def9d4487b3',
                                                      client_secret='f954aa59c7dd468ca6867d2b3024433b')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

CONTAINER = []
for playlist in PLAYLISTS:
    Name, Link, playlistid = playlist
    playlistcard = []
    count = 0
    PlaylistLink = "http://www.youtube.com/watch_videos?video_ids="
    for i in (sp.playlist_tracks(Link)['items']):
        if count == 50:
            break
        try:
            song = i['track']['name'] + i['track']['artists'][0]['name']
            songdic = (YoutubeSearch(song, max_results=1).to_dict())[0]
            playlistcard.append(
                [songdic['thumbnails'][0], songdic['title'], songdic['channel'], songdic['id']])
            PlaylistLink += songdic['id'] + ','
        except:
            continue
        count += 1

    from urllib.request import urlopen
    req = urlopen(PlaylistLink)
    PlaylistLink = req.geturl()
    print(PlaylistLink)
    PlaylistId = PlaylistLink[PlaylistLink.find('list')+5:]

    CONTAINER.append([Name, playlistcard, playlistid])


json.dump(CONTAINER, open('card.json', 'w'), indent=6)

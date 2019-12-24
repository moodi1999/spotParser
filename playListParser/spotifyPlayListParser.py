
import requests
from bs4 import BeautifulSoup
import json
import re
import glob
from path import path
from collections import namedtuple
import urllib.request
import urllib.error
import urllib.parse
import asyncio
from pyppeteer import launch

def getAlbumTrackData(tracks):
    tracksData: dict = None
    for track in tracks:
        trackData = track
        artists = trackData['artists']
        artistName = None
        if len(artists) != 0:
            for artist in artists:
                if artist['type'] == 'artist':
                    artistName = artist['name']
                    break

            if artistName is None:
                artistName = artists[0]

    return tracksData 

def getPlayListTrackData(tracks):
    tracksData: dict = None
    for track in tracks:
        trackData = track
        artists = trackData['artists']
        artistName = None
        if len(artists) != 0:
            for artist in artists:
                if artist['type'] == 'artist':
                    artistName = artist['name']
                    break

            if artistName is None:
                artistName = artists[0]

    return tracksData            

def getData(jsonData):
    dataType = jsonData['type']
    name = jsonData['name']
    
    result = {'type': dataType, 'name': name}
    
    if dataType == 'album':
        image = jsonData['images']
        if len(image) != 0:
            image = image[-1]

        result.update({'releaseDate': jsonData['release_date'], 'converImage': image, 'tracks':  getAlbumTrackData(jsonData['tracks'])})
    else:
        result.update({'tracks': getPlayListTrackData(jsonData['tracks'])})

    return result


def getTrackSearchKey(url):
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')

    path('HTMLContent.html').write_bytes(soup.encode())
    htmlJsonContent = re.findall(
        r"Spotify\.Entity\s\=\s([\s\S]*?)\;", str(soup))[0]

    dataDic = json.loads(htmlJsonContent)

    # if dataDic['type'] == 'album':
    #     getAlbumData(dataDic)
    # else if dataDic['type'] == 'playlist'
    #     f
        
    items = dataDic['tracks']['items']

    path('jsonData.json').write_bytes(htmlJsonContent.encode())

    trackSearchKey: list = []
    for item in items:
        if (dataDic['type'] == 'album'):
            artistName = item['artists'][0]['name']
            trackName = item['name']
            trackSearchKey.append(artistName + " " + trackName)
        else:
            artistName = item['track']['artists'][0]['name']
            trackName = item['track']['name']
            trackSearchKey.append(artistName + " " + trackName)
    
    return trackSearchKey

if __name__ == "__main__":
    
    url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'
    url = 'https://open.spotify.com/playlist/37i9dQZF1DX8NTLI2TtZa6'
    url = 'https://open.spotify.com/album/5UACk85y1hNRSUtY0ss8pb'
    # url = 'https://api.spotify.com/v1/playlists/37i9dQZF1DX8NTLI2TtZa6/tracks?offset=100&limit=100&market=FR&locale=en'
    searchKeys = getTrackSearchKey(url)

    tracks = json.dumps(searchKeys)
    txtFiles = glob.glob('**/*.txt', recursive=True)
    path('trackSearchKey.txt').write_bytes(tracks.encode())

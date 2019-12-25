
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


def getArtistName(artists):
    artistName = None
    if len(artists) != 0:
        for artist in artists:
            if artist['type'] == 'artist':
                artistName = artist['name']
                break

        if artistName is None:
            artistName = artists[0]
    return artistName


def getAlbumTrackData(track):
    tracksData: dict = {}

    artistName = getArtistName(track['artists'])

    image = getImageConver(track['images'])

    tracksData.update({'name': track['name'],
                       'artist': artistName,
                       'coverImage': image,
                       'releaseDate': track['release_date']
                       })

    return tracksData


def getPlayListTrackData(item):
    tracksData: dict = {}

    if item['track']['type'] == 'track':
        track = item['track']
        artistName = getArtistName(track['artists'])
        trackName = track['name']

        albumTrackData = getAlbumTrackData(track['album'])

        tracksData.update(
            {
                'artistName': artistName,
                'trackAlbumData': albumTrackData,
                'trackName': trackName
            })
    return tracksData


def getImageConver(images):
    image = None
    if len(images) == 1:
        image = images[0]
    elif len(images) >= 2:
        image = images[-2]

    return image


def getData(jsonData):
    dataType = jsonData['type']
    name = jsonData['name']

    result = {'type': dataType, 'name': name}

    if dataType == 'album':
        tracksData = []
        for track in jsonData['tracks']['items']:
            tracksData.append(getAlbumTrackData(track))

        result.update({
            'tracks':  tracksData,
        })

    else:
        tracksData = []
        for track in jsonData['tracks']['items']:
            tracksData.append(getPlayListTrackData(track))

        result.update({
            'tracks': tracksData
        })

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

    tracks = getData(dataDic)

    items = dataDic['tracks']['items']

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

    return {'trackSearchKey': trackSearchKey,
            "tracksInfo": tracks}


if __name__ == "__main__":

    url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'
    url = 'https://open.spotify.com/album/5UACk85y1hNRSUtY0ss8pb'
    url = 'https://open.spotify.com/playlist/37i9dQZF1DX8NTLI2TtZa6'
    # url = 'https://api.spotify.com/v1/playlists/37i9dQZF1DX8NTLI2TtZa6/tracks?offset=100&limit=100&market=FR&locale=en'
    searchKeys = getTrackSearchKey(url)

    tracks = json.dumps(searchKeys['trackSearchKey'])
    tracksInfo = json.dumps(searchKeys['tracksInfo'])

    path('tracksInfo.json').write_bytes(tracksInfo.encode())

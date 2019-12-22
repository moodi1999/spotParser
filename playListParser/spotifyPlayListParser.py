
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

def getTrackSearchKey(url):
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')

    htmlJsonContent = re.findall(
        r"Spotify\.Entity\s\=\s([\s\S]*?)\;", str(soup))[0]

    dataDic = json.loads(htmlJsonContent)

    items = dataDic['tracks']['items']

    trackSearchKey: list = []
    for item in items:
        artistName = item['track']['artists'][0]['name']
        trackName = item['track']['name']
        trackSearchKey.append(artistName + " " + trackName)
    
    return trackSearchKey

if __name__ == "__main__":
    
    url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'
    searchKeys = getTrackSearchKey(url)

    tracks = json.dumps(searchKeys)
    path('trackSearchKey.txt').write_bytes(tracks.encode())


import requests
from bs4 import BeautifulSoup
import json
import re
from path import path
import glob
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

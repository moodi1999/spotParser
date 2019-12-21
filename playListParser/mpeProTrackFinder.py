
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

def getTrackPage(trackSearchKey):
    searchKeyWork = trackSearchKey.replace(" ", "-")
    url = "https://mp3paw.com/mp3-download/" + searchKeyWork
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    trackId = re.findall(
        r"\s*content\=\"https:\/\/img\.youtube\.com\/vi\/(\w+)\/maxresdefault\.jpg\"", str(soup))[0]
    return "https://mp3pro.xyz/" + trackId

def getDownloadLink(trackSearchKey):
    searchKeyWork = trackSearchKey.replace(" ", "-")
    url = "https://mp3paw.com/mp3-download/" + searchKeyWork
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    trackId = re.findall(
        r"\s*content\=\"https:\/\/img\.youtube\.com\/vi\/(\w+)\/maxresdefault\.jpg\"", str(soup))[0]
    return "https://mp3pro.xyz/" + trackId
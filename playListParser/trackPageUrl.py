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
import time
from pyppeteer import launch


def getTrackPage(trackSearchKey):
    try:
        url = "https://mp3paw.com/mp3-download/" + trackSearchKey
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        trackId = re.findall(
            r"\s*content\=\"https:\/\/img\.youtube\.com\/vi\/([\s\S]*?)\/maxresdefault\.jpg\"", str(soup))[0]
        pageUrl = "https://mp3pro.xyz/" + trackId
        print("got -> ", pageUrl)
        return pageUrl
    except Exception as e:
            msg = "Exception is:\n %s \n" % e
            time.sleep(10)
            print(msg)

    return ""


if __name__ == "__main__":
    
    txtFiles = glob.glob('**/*.txt', recursive=True)
    spotifyTracksPath = ""
    for f in txtFiles:
        if 'trackSearchKey.txt' == f:
            spotifyTracksPath = f
    
    content = path(spotifyTracksPath).bytes().decode("utf-8")
    spotifyTracks = json.loads(content)

    tracksPageUrl:list = []
    for key in spotifyTracks:
        pageUrl = getTrackPage(key)
        if pageUrl != "":
            tracksPageUrl.append(pageUrl)
    
    pageUrls = json.dumps(tracksPageUrl)
    path('trackPageUrls.txt').write_bytes(pageUrls.encode())

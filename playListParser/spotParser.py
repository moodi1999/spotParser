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

from spotifyPlayListParser import getTrackSearchKey
from mp3ProTrackFinder import getTrackIdAndToken
from mp3ProTrackFinder import getTrackPage


if __name__ == "__main__":
    
    url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'
    searchKeys = getTrackSearchKey(url)

    tracksPageUrl:list = []
    for key in searchKeys:
        pageUrl = getTrackPage(key)
        tracksPageUrl.append(pageUrl)
    
    pageUrls = json.dumps(tracksPageUrl)
    path('trackUrls.txt').write_bytes(pageUrls.encode())

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(getTrackIdAndToken(tracksPageUrl))

    # https://mp3pro.xyz/download?
    # v=COOBN-cdJbo&
    # t=d0277824e713bae3af32fd50c75bf82f&
    # f=0&
    # d=0&
    # r=https%3A%2F%2Fmp3pro.xyz%2FCOOBN-cdJbo&
    # b=320&
    # _=1577007959990&
    # cid=1397400876.1569142253

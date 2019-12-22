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

# from playListParser.spotifyPlayListParser import getTrackSearchKey
from mp3ProTrackFinder import getTrackIdAndToken


if __name__ == "__main__":
    
    # url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'
    # searchKeys = getTrackSearchKey(url)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(getTrackIdAndToken("https://mp3pro.xyz/COOBN-cdJbo"))

    print(result)

    # https://mp3pro.xyz/download?
    # v=COOBN-cdJbo&
    # t=d0277824e713bae3af32fd50c75bf82f&
    # f=0&
    # d=0&
    # r=https%3A%2F%2Fmp3pro.xyz%2FCOOBN-cdJbo&
    # b=320&
    # _=1577007959990&
    # cid=1397400876.1569142253

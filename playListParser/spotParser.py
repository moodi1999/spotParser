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

from playListParser.spotifyPlayListParser import getTrackSearchKey
from playListParser.spotifyPlayListParser import getTrackSearchKey


if __name__ == "__main__":
    
    url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'
    searchKeys = getTrackSearchKey(url)

    for key in searchKeys:


    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(extract_all(languages))
    pprint.pprint(result)

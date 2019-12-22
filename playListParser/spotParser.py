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

if __name__ == "__main__":
    
    txtFiles = glob.glob('**/*.txt', recursive=True)
    tracksDownloadUrl = ""
    for f in txtFiles:
        if 'tracksDownloadUrl.txt' == f:
            tracksDownloadUrl = f
    
    content = path(tracksDownloadUrl).bytes().decode("utf-8")
    tracks = json.loads(content)

    tracksTxt = ""
    for t in tracks:
        tracksTxt = tracksTxt + t + '\n'
    
    path('ADMLinks.txt').write_bytes(tracksTxt.encode())

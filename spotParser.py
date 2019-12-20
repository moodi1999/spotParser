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


async def main(pageUrl):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(pageUrl)
    # a = page.cookies
    # print(a)
    await page.screenshot({'path': 'example.png'})
    await browser.close()

url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'

# open with GET method
resp = requests.get(url)

# http_respone 200 means OK status
if resp.status_code == 200:

    # we need a parser,Python built-in HTML parser is enough .
    soup = BeautifulSoup(resp.text, 'html.parser')

    # path('newJson2.html').write_bytes(soup.encode())

    htmlJsonContent = re.findall(
        r"Spotify\.Entity\s\=\s([\s\S]*?)\;", str(soup))[0]

    dataDic = json.loads(htmlJsonContent)

    items = dataDic['tracks']['items']

    trackSearchKey: list = []
    for item in items:
        artistName = item['track']['artists'][0]['name']
        trackName = item['track']['name']
        trackSearchKey.append(artistName + " " + trackName)

    trackPages: list = []
    print(trackPages)
    for track in trackSearchKey:
        searchKeyWork = track.replace(" ", "-")
        url = "https://mp3paw.com/mp3-download/" + searchKeyWork
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        trackId = re.findall(r"\s*content\=\"https:\/\/img\.youtube\.com\/vi\/(\w+)\/maxresdefault\.jpg\"", str(soup))[0]
        trackPage = "https://mp3pro.xyz/" + trackId
        trackPages.append(trackPage)
    
    for page in trackPages:
        print(page)


else:
    print("Error")


# url = 'https://open.spotify.com/playlist/5KhkvPjNVE3dOtvvAo6IWC?si=BYohF3T0SGyV4LGzKfhgCA'

# response = urllib.request.urlopen(url)
# webContent = response.read()

# path('newHtml.html').write_bytes(str(webContent).encode())

# htmlFile = glob.glob('**/*.html', recursive=True)
# htmlContent = path(htmlFile[0]).bytes().decode("utf-8")


# path('newJson.json').write_bytes(htmlJsonContent.encode())

# dataDic = json.loads(str(htmlJsonContent))

# print(dataDic)


# htmlFile = glob.glob('**/*.html', recursive=True)
# htmlContent = path(htmlFile[0]).bytes().decode("utf-8")

# path('newJson.json').write_bytes(htmlJsonContent.encode())

# jsonFile = glob.glob('**/*.json', recursive=True)

# jsonContent = path(jsonFile[0]).bytes().decode("utf-8")

# data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

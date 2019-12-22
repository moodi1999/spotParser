
import requests
from bs4 import BeautifulSoup
import json
import re
import glob
from collections import namedtuple
import urllib.request
import urllib.error
import urllib.parse
import asyncio
from pyppeteer import launch
from requests import Session


async def get_browser():
    return await launch({"headless": False})


async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    return page


async def getIdsAndTokens(browser, url):
    page = await get_page(browser, url)
    cookie = await page.cookies()

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    ajaxCookieIdAndToken = re.findall(
        r"\"token\"\:\"([\s\S]*?\:[\s\S]*?)\"", str(soup))[0]

    result = {
        "trackId": str(ajaxCookieIdAndToken.split(":")[0]),
        "token": str(ajaxCookieIdAndToken.split(":")[1]),
        "__cfduid": str(cookie[0]['value']),
        "_gid": str(cookie[1]['value']),
        "_ga": str(cookie[2]['value']),
        "_gat_gtag_UA_154873324_1": str(cookie[3]['value'])
    }
    return result


async def getTrackIdAndToken(trackPageUrl):
    browser = await get_browser()
    params = await getIdsAndTokens(browser, trackPageUrl)
    getAudioToken(params)
    return 


def getAudioToken(headerParams):
    session = Session()
    
    response = session.post(
        url="https://mp3pro.xyz/ajax",
        data="purpose=audio&token=" + headerParams['trackId'] + "%3A" + headerParams['token'],
        headers={
            'authority': "mp3pro.xyz",
            'pragma': "no-cache",
            'cache-control': "no-cache",
            'accept': "application/json, text/javascript, */*; q=0.01",
            'origin': "https://mp3pro.xyz",
            'x-requested-with': "XMLHttpRequest",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'referer': "https://mp3pro.xyz/5lNgGfPtako",
            'accept-language': "en-US,en;q=0.9,fa;q=0.8",
            'cookie': "__cfduid=" + headerParams['__cfduid'] +"; _y_blocked=_; _ga="+ headerParams['_ga'] +"; _gid=" + headerParams['_gid']
        }
    )
    idAndToken = json.loads(str(response.text))
    trackId = idAndToken['audio'].split(":")[0]
    audioToken = idAndToken['audio'].split(":")[1]
    return {"trackId": trackId, "audioToken": audioToken}

def getTrackPage(trackSearchKey):
    searchKeyWork = trackSearchKey.replace(" ", "-")
    url = "https://mp3paw.com/mp3-download/" + searchKeyWork
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    trackId = re.findall(
        r"\s*content\=\"https:\/\/img\.youtube\.com\/vi\/([\s\S]*?\:[\s\S]*?)\/maxresdefault\.jpg\"", str(soup))[0]
    return "https://mp3pro.xyz/" + trackId
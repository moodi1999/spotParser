
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
from requests import Session

def patch_pyppeteer():
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


async def get_browser():
    return await launch({"headless": False})


async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    return page


async def getIdsAndTokens(browser, url):
    page = await get_page(browser, url)
    print("opened " + url)
    cookie = await page.cookies()

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    ajaxCookieIdAndToken = re.findall(
        r"\"token\"\:\"([\s\S]*?\:[\s\S]*?)\"", str(soup))[0]

    result = {
        "url": url,
        "trackId": str(ajaxCookieIdAndToken.split(":")[0]),
        "token": str(ajaxCookieIdAndToken.split(":")[1]),
        "__cfduid": str(cookie[0]['value']),
        "_gid": str(cookie[1]['value']),
        "_ga": str(cookie[2]['value']),
        "_gat_gtag_UA_154873324_1": str(cookie[3]['value'])
    }
    print("closingPage")
    await page.close()
    return result


async def getTrackIdAndToken(trackPageUrls):
    browser = await get_browser()

    downloadLinks: list = []
    for url in trackPageUrls:
        try:
            print("getting data for " + url)

            result: dict = await getIdsAndTokens(browser, url)
            result.update({"audioToken": getAudioToken(result)})
            
            link = "https://mp3pro.xyz/download?"
            tId = "v=" + result['trackId'] + "&"
            audioToken = "t=" + result['audioToken'] + "&"
            f = "f=" + str(0) + "&"
            d = "d=" + str(0) + "&"
            r = "r=" + result['url'] + "&"
            b = "b=" + str(320) + "&"
            underLine = "_=" + str(0) + "&"
            cid = "cid=" + ""

            downloadLink = link + tId + audioToken + f + d + r + b + underLine + cid
            print("got download link for " + url + "  -> " + downloadLink)
            downloadLinks.append(downloadLink)

            downloadJsonLinks = json.dumps(downloadLinks)
            path('tracksDownloadUrl.txt').write_bytes(downloadJsonLinks.encode())
        except Exception as e:
            msg = "error for " + url + "Exception is:\n %s \n" % e
            print(msg)

    return downloadLinks


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
    audioToken = idAndToken['audio'].split(":")[1]
    return audioToken


if __name__ == "__main__":
    
    txtFiles = glob.glob('**/*.txt', recursive=True)
    trackUrlsPath = ""
    for f in txtFiles:
        if 'trackPageUrls.txt' == f:
            trackUrlsPath = f
    
    content = path(trackUrlsPath).bytes().decode("utf-8")
    tracksPageUrl = json.loads(content)

    patch_pyppeteer()

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

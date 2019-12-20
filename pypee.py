# import asyncio
# from pyppeteer import launch

# async def main():
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto("https://mp3pro.xyz/5lNgGfPtako")
#     await page.screenshot({'path': 'example.png'})
#     element = await page.$$('a')
#     print(elemetn)
#     await browser.close()

# asyncio.get_event_loop().run_until_complete(main())
# https://mp3pro.xyz/
# download?
# v=5lNgGfPtako&
# t=93f6d73b2628c8b0e9cb68d8f830a30a&
# f=0&
# d=0&
# r=https%3A%2F%2Fmp3pro.xyz%2F5lNgGfPtako&
# b=320&
# _=1576831926591&
# cid=604422947.1576831157
from pybrowser import Browser
import requests
from bs4 import BeautifulSoup
import json
import re
from collections import namedtuple
import urllib.request
import urllib.error
import urllib.parse
import asyncio
from pyppeteer import launch

with Browser(browser_name=Browser.IE) as b:
    b.goto("https://mp3pro.xyz/5lNgGfPtako")
    cookie = b.cookies
    # __cfduid = cookie[0]['value']
    # _ga = cookie[1]['value']
    # _ga2 = cookie[2]['value']
    # _ga3 = cookie[3]['value']
    
    soup = BeautifulSoup(b.content, 'html.parser')
    audioToken = re.findall(r"\"token\"\:\"(\w+\:\w+)\"", str(soup))[0]
    trackId = audioToken.split(":")[0]
    token = audioToken.split(":")[1]
    print(audioToken.split(":"))
    for c in cookie:
        print(c)

        
# url = "https://mp3pro.xyz/ajax"

# payload = "purpose=audio%5E&token=5lNgGfPtako%5E%25%5E3A0dac7314789503e23e812c195cc8e904"
# headers = {
#     'authority': "mp3pro.xyz",
#     'accept': "application/json, text/javascript, */*; q=0.01",
#     'origin': "https://mp3pro.xyz",
#     'x-requested-with': "XMLHttpRequest",
#     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
#     'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
#     'sec-fetch-site': "same-origin",
#     'sec-fetch-mode': "cors",
#     'referer': "https://mp3pro.xyz/5lNgGfPtako",
#     'accept-encoding': "gzip, deflate, br",
#     'accept-language': "en-US,en;q=0.9,fa;q=0.8",
#     'cookie': "__cfduid=de0a70ba2802a97240de0c3ddd70406891576008698; _y_blocked=_a; _ga=GA1.2.821959684.1576036957; _gid=GA1.2.304682522.1576778501; dl_secure=ok",
#     'authorization': "B426F5AEA8907526F3B2FAD8A94EAD86D2255C2632704169227D702F69D10338B81D4CC7094207CD5769A5198224C0231564FA2F67EA0586FD72F10D81590C7D",
#     'ostype': "1",
#     'appid': "1",
#     'sessionid': "122368"
#     }

# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)
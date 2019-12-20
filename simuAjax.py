from requests import Session

session = Session()

# HEAD requests ask for *just* the headers, which is all you need to grab the
# session cookie
session.head('http://sportsbeta.ladbrokes.com/football')

response = session.post(
    url="https://mp3pro.xyz/ajax",
    data="purpose=audio&token=5lNgGfPtako%3A0dac7314789503e23e812c195cc8e904",
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
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9,fa;q=0.8",
        'cookie': "__cfduid=d52549edb2b3c33231ccf0c00dc9362a41576830271; _y_blocked=_; _ga=GA1.2.604422947.1576831157; _gid=GA1.2.2057369448.1576831157"
    }
)

print(response.text)
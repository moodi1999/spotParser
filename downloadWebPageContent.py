import json
import re
from path import path
import glob
from collections import namedtuple
import urllib.request, urllib.error, urllib.parse

url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
url = 'https://printatestpage.com/'


response = urllib.request.urlopen(url)
webContent = response.read()

path('newJson2.html').write_bytes(str(webContent).encode())

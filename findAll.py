from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import sys

try:
    html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
except HTTPError as e:
    print(e)
    sys.exit(1)

bs = BeautifulSoup(html.read(), 'html.parser')
nameList = bs.findAll('span',{'class' : 'green'})
for name in nameList:
    print(name.get_text())
        



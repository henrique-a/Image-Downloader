import os
import requests
import urllib
from bs4 import BeautifulSoup

url = input('URL: ')
html = requests.get(url)
html_text = html.text
soup = BeautifulSoup(html_text, 'html.parser')

imgs = soup.findAll('img', {'src': True})

if not os.path.isdir('img'):
    os.mkdir('img')
i = 0
name = input('Name to save image: ')
for img in imgs:
    img_url = img['src']
    if img_url.startswith('http'): 
        i = i + 1
        f = open('img/' + name + str(i) + '.jpg','wb')
        f.write(urllib.request.urlopen(img_url).read())
        f.close()

import os
import requests
import urllib
from urllib.parse import urlparse 
from bs4 import BeautifulSoup

def get_extension(img_url):
    path = urlparse(img_url).path
    ext = os.path.splitext(path)[1]
    return ext

def main():
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
        if not img_url.startswith('http'):
            img_url = url + img_url
        print('Saving image: ' + img_url) 
        i = i + 1
        ext = get_extension(img_url)
        f = open('img/' + name + ' - ' + str(i) + ext, 'wb')
        try:
            f.write(urllib.request.urlopen(img_url).read())
        except urllib.error.HTTPError:
            print('Image ' + img_url + ' not found')

        f.close()

if __name__ == '__main__':
    main()
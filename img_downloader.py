import os
import requests
import urllib
from urllib.parse import urlparse 
from bs4 import BeautifulSoup

i = 0 # Image counter
def get_extension(img_url):
    path = urlparse(img_url).path
    ext = os.path.splitext(path)[1]
    return ext

def save_image(url, img_url, name):
    if not img_url.startswith('http'):
        img_url = url + img_url
    print('Saving image: ' + img_url) 
    global i
    i = i + 1
    ext = get_extension(img_url)
    f = open('img/' + name + ' - ' + str(i) + ext, 'wb')
    try:
        f.write(urllib.request.urlopen(img_url).read())
    except urllib.error.HTTPError:
        print('Image ' + img_url + ' not found')
    except ConnectionResetError:
        print('Connection interrupted')

    f.close()    

def main():
    url = input('URL: ')
    html = requests.get(url)
    html_text = html.text
    soup = BeautifulSoup(html_text, 'html.parser')
    if not os.path.isdir('img'):
        os.mkdir('img')

    imgs = soup.findAll('img', {'src': True})
    name = input('Name to save image: ')
    for img in imgs:
        img_url = img['src']
        save_image(url, img_url, name)

    # Find images in links
    links = soup.findAll('a', {'href': True})
    for link in links:
        if link.findAll('img'):
            img_url = link['href']
            save_image(url, img_url, name)

if __name__ == '__main__':
    main()
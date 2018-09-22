import os
import urllib
from bs4 import BeautifulSoup
import dryscrape

i = 0 # Image counter
def get_extension(img_url):
    formats = ['.jpg', '.jpeg', '.png', '.tiff', '.gif', '.svg']
    ext = '.' + img_url.split('.')[-1]
    if not ext in formats:
        return '' 
    return ext 

def save_image(url, img_url, name):

    if img_url.startswith('//'):
        img_url = 'http:' + img_url

    elif img_url.startswith('/'):
        img_url = url + img_url

    ext = get_extension(img_url)

    if ext:
        print('Saving image: ' + img_url) 
        global i
        i = i + 1
        f = open('img/' + name + ' - ' + str(i) + ext, 'wb')
        try:
            f.write(urllib.request.urlopen(img_url).read())
        except urllib.error.HTTPError:
            print('Image ' + img_url + ' not found')
        except ConnectionResetError:
            print('Connection interrupted')
        except urllib.error.URLError:
            print('Operation timed out')

        f.close()    

def main():
    url = input('URL: ')
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    soup = BeautifulSoup(response, "html.parser")
    if not os.path.isdir('img'):
        os.mkdir('img')

    name = input('Name to save image: ')

    # Find images in links
    links = soup.findAll('a', {'href': True})
    for link in links:
        if link.findAll('img'):
            img_url = link['href']
            save_image(url, img_url, name)
    
    # Find images in <img> tags
    imgs = soup.findAll('img', {'src': True})
    for img in imgs:
        img_url = img['src']
        save_image(url, img_url, name)
    
if __name__ == '__main__':
    main()
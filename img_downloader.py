import os
from queue import Queue
import threading as th
import urllib
import urllib.request
from bs4 import BeautifulSoup
import dryscrape

i = 0 # Image counter
NUMBER_OF_THREADS = 8
queue = Queue()

def get_extension(img_url):
    formats = ['.jpg', '.jpeg', '.png', '.tiff', '.gif', '.svg']
    ext = '.' + img_url.split('.')[-1]
    if not ext in formats:
        return '' 
    return ext 

# Create worker threads
def create_workers(url, name):
    for _ in range(NUMBER_OF_THREADS):
        t = th.Thread(target=work, args=(url, name))
        t.start()

# Do the next job in the queue
def work(url, name):
    while not queue.empty():
        img_url = queue.get()
        save_image(url, img_url, name)
        queue.task_done()


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
    name = input('Name to save images: ')

    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    soup = BeautifulSoup(response, "html.parser")
    if not os.path.isdir('img'):
        os.mkdir('img')

    # Find images in links
    links = soup.findAll('a', {'href': True})
    for link in links:
        if link.findAll('img'):
            img_url = link['href']
            queue.put(img_url)
    
    # Find images in <img> tags
    imgs = soup.findAll('img', {'src': True})
    for img in imgs:
        img_url = img['src']
        queue.put(img_url)

    create_workers(url, name)

if __name__ == '__main__':
    main()
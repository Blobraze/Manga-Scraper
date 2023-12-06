import urllib.request
import requests
from PIL import Image
from bs4 import BeautifulSoup
import flet as ft

# Download image from url
'''opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
urllib.request.install_opener(opener)
urllib.request.urlretrieve( 
  'https://asuratoon.com/wp-content/uploads/2023/07/0000GN00000.jpg', 
   'test.jpg') 
  
img = Image.open('test.jpg') 
img.show()'''

# Open image from url
'''my_url = "https://asuratoon.com/wp-content/uploads/2023/07/0000GN00000.jpg"

# Open the image directly from the URL using Pillow
my_img = Image.open(requests.get(my_url, stream=True).raw)

# Show the image
my_img.show()'''

URL = "https://asuratoon.com/manga/?page=1&order=title"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
comics = soup.find_all(class_='bs')

images_links = []

for comic in comics:
    images_links.append((comic.find('img', class_="ts-post-image wp-post-image attachment-medium size-medium"))['src'])

x = 1
for image_link in images_links:
  opener = urllib.request.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
  urllib.request.install_opener(opener)
  urllib.request.urlretrieve(image_link, f'./covers/{x}.png')
  x += 1

#print(images_links)

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.update()

ft.app(target=main)
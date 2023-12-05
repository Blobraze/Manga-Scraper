import urllib.request
import requests
from PIL import Image
from bs4 import BeautifulSoup

# Download image from url
'''opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
urllib.request.install_opener(opener)
urllib.request.urlretrieve( 
  'https://asuratoon.com/wp-content/uploads/2023/07/0000GN00000.jpg', 
   'test.jpg') 
  
img = Image.open('test.jpg') 
img.show()'''

my_url = "https://asuratoon.com/wp-content/uploads/2023/07/0000GN00000.jpg"

# Open the image directly from the URL using Pillow
my_img = Image.open(requests.get(my_url, stream=True).raw)

# Show the image
my_img.show()
import requests
from bs4 import BeautifulSoup
import flet as ft

URL = "https://asuratoon.com/manga/list-mode/"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
comic_links_list = soup.find(class_="mrgn").find('div', class_="soralist").find_all('div', class_="blix")

links = []
titles = []

for blix in comic_links_list:
    comics = blix.find_all('a', class_="series")
    for comic in comics:
        links.append(comic["href"])
        titles.append(comic.text)

'''x = 1
for title in titles:
    print(f'{x}. {title}')
    x += 1'''

'''option = input("Choose manga: ")
print(links[int(option)-1])'''

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    for title in titles:
        t = ft.Text(value=title + '\n' + links[titles.index(title)], color="green")
        page.controls.append(t)
    page.update()

ft.app(target=main)



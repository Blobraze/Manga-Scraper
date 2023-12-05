import requests
from bs4 import BeautifulSoup
import json
import smtplib
import ssl
from email.message import EmailMessage

to_read_list = []

x = 0

with open('../mangi.json', 'r+') as mangas:
    mangas_loaded = json.load(mangas)
    while x < len(mangas_loaded['mangas']):
        changed = False

        URL = mangas_loaded['mangas'][0]['link']

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        manga_name = soup.find(class_='entry-title')
        chapter_list_find = soup.find(class_='clstyle')
        chapter_data_find = chapter_list_find.find_all('a')

        if "chapters" in mangas_loaded['mangas'][0]:
            chapters = mangas_loaded['mangas'][0]['chapters']
        else:
            chapters = 0

        for ch_data in chapter_data_find:
            ch_name = ch_data.find('span', class_='chapternum')
            ch_date = ch_data.find('span', class_='chapterdate')
            text = ch_name.text + '\n' + ch_date.text
            ch_link = ch_data['href']

            ch_number = ch_name.text.split(' ')

            # sprawdz numer rozdzialu
            last_chapter = chapters
            if float(ch_number[1]) > chapters:
                chapters = float(ch_number[1])

            if ("chapters" in mangas_loaded['mangas'][0]) and (chapters > mangas_loaded['mangas'][0]['chapters']):
                if {"name": mangas_loaded["mangas"][0]['name'], "chapters": (chapters - mangas_loaded['mangas'][0]['chapters'])} not in to_read_list:
                    to_read_list.append({"name": mangas_loaded["mangas"][0]['name'],
                                         "chapters": (chapters - mangas_loaded['mangas'][0]['chapters']),
                                         "link": mangas_loaded['mangas'][0]['link']})
                else:
                    continue

                changes = {"name": manga_name.text, "link": mangas_loaded['mangas'][0]['link'], "chapters": chapters}
                changed = True

            else:
                changes = {"name": manga_name.text, "link": mangas_loaded['mangas'][0]['link'], "chapters": chapters}
                changed = True

        # print(chapters)

        if changed:
            del mangas_loaded['mangas'][0]
            mangas_loaded['mangas'].append(changes)
            mangas.seek(0)
            json.dump(mangas_loaded, mangas, indent=4)
            changed = False

        x += 1

message = ''
for i in range(len(to_read_list)):
    message += to_read_list[i]['name']
    message += f"\nNieprzeczytane: {to_read_list[i]['chapters']}\n\n"
    i += 1

# print(message)

port = 465  # For starttls
sender_email = "mangascraper2@gmail.com"
receiver_email = "mateuszgrzeszyk@gmail.com"
password = "vwts epxp krts wccl"

msg = EmailMessage()

if message != '':
    msg.set_content(message)
else:
    msg.set_content('Nic nowego.')

smtp_server = "smtp.gmail.com"
msg['Subject'] = 'Nieprzeczytane'
msg['From'] = sender_email
msg['To'] = receiver_email

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.send_message(msg)

# TODO:
# 1. Lista linkow
# 2. Pobierz i wyslij obrazy w archiwum

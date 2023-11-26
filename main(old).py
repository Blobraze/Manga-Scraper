import requests
from bs4 import BeautifulSoup
import json
import smtplib
import ssl
from email.message import EmailMessage

# from email.message import EmailMessage

to_read_list = []

x = 0

with open('mangi.json', 'r+') as mangas:
    mangas_loaded = json.load(mangas)
    print(len(mangas_loaded['mangas']))
    for x in range(0, len(mangas_loaded['mangas'])):
        print(x)
        changed = False

        URL = mangas_loaded['mangas'][x]['link']

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        manga_name = soup.find(class_='entry-title')
        chapter_list_find = soup.find(class_='clstyle')
        chapter_data_find = chapter_list_find.find_all('a')

        if "chapters" in mangas_loaded['mangas'][x]:
            chapters = mangas_loaded['mangas'][x]['chapters']
        else:
            chapters = 0

        for ch_data in chapter_data_find:
            ch_name = ch_data.find('span', class_='chapternum')
            ch_date = ch_data.find('span', class_='chapterdate')
            text = ch_name.text + '\n' + ch_date.text
            ch_link = ch_data['href']

            ch_number = ch_name.text.split(' ')

            # sprawdz numer rozdzialu
            if float(ch_number[1]) > chapters:
                chapters = float(ch_number[1])

            if ("chapters" in mangas_loaded['mangas'][x]) and (chapters > mangas_loaded['mangas'][x]['chapters']):
                if {"name": mangas_loaded["mangas"][x]['name'], "chapters": (chapters - mangas_loaded['mangas'][x]['chapters'])} not in to_read_list:
                    to_read_list.append({"name": mangas_loaded["mangas"][x]['name'],
                                         "chapters": (chapters - mangas_loaded['mangas'][x]['chapters'])})
                else:
                    continue

                changes = {"name": manga_name.text, "link": mangas_loaded['mangas'][x]['link'], "chapters": chapters}
                changed = True

            else:
                changes = {"name": manga_name.text, "link": mangas_loaded['mangas'][x]['link'], "chapters": chapters}
                changed = True

        # print(chapters)

        if changed:
            print(mangas_loaded['mangas'])
            del mangas_loaded['mangas'][x]
            print(mangas_loaded['mangas'])
            mangas_loaded['mangas'].append(changes)
            print(mangas_loaded['mangas'])
            mangas.seek(0)
            json.dump(mangas_loaded, mangas, indent=4)
            changed = False

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

if message != '':
    msg = EmailMessage()
    msg.set_content(message)
    smtp_server = "smtp.gmail.com"
    msg['Subject'] = 'Nieprzeczytane'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

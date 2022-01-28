import requests
from bs4 import BeautifulSoup
import os
import telegram

ac_home_url = os.environ['AC_HOME_URL']
my_tg_token = os.environ['MY_TG_TOKEN']
my_tg_chatID = os.environ['MY_TG_CHATID']
bot = telegram.Bot(token=my_tg_token)

print("Reading text file...")
with open('manga_urls.txt') as f:
    mangalist = f.read().splitlines()

home_url = ac_home_url
items = []
titles_ita = []
italy_statuses = []
next_releases = []
next_releases_dates = []
latest_releases = []
latest_releases_dates = []

print("Fetching dates...")
for manga in mangalist:
    response = requests.get(manga)
    soup = BeautifulSoup(response.text, 'html.parser')
    titolo_italiano = soup.find('h1').getText()
    stato_ita = soup.find(text="Stato in Italia")
    stato_ita_td = stato_ita.parent
    target_statoIt = stato_ita_td.find_next_sibling('dd').text
    titles_ita.append(titolo_italiano.strip())
    italy_statuses.append(target_statoIt.strip())
    if target_statoIt.strip() == "in corso" and soup.find(text="Prossima uscita") is not None:
        next_releases_text = soup.find('h3').getText()
        next_releases.append(next_releases_text.strip())
        next_release_link = soup.select_one("a[href*=edizione\/]")
        next_releases_dates.append(home_url+next_release_link.get('href'))
        latest_releases.append("")
        latest_releases_dates.append("N.D.")
    elif target_statoIt.strip() == "completato" and soup.find(text="Prossima uscita") is not None:
        next_releases_text = soup.find('h3').getText()
        next_releases.append(next_releases_text.strip())
        next_release_link = soup.select_one("a[href*=edizione\/]")
        next_releases_dates.append(home_url+next_release_link.get('href'))
        latest_releases.append("")
        latest_releases_dates.append("N.D.")
    elif soup.find(text="Ultima uscita") is not None:
        latest_releases_text = soup.find('h3').getText()
        latest_releases.append("Ultima uscita: "+latest_releases_text.strip())
        next_release_link = soup.select_one("a[href*=edizione\/]")
        latest_releases_dates.append(home_url+next_release_link.get('href'))
        next_releases.append("")
        next_releases_dates.append("N.D.")
    else:
        next_releases.append("")
        next_releases_dates.append("N.D.")
        latest_releases.append("")
        latest_releases_dates.append("N.D.")
        continue

print("Formatting strings...")
next_volume_dates = []
latest_volume_dates = []
for item in next_releases_dates:
    if item != "N.D.":
        response_next = requests.get(item)
        soup_next = BeautifulSoup(response_next.text, 'html.parser')
        next_date_parent = soup_next.find('strong', text="Data pubblicazione:")
        next_volume_dates.append(next_date_parent.next_sibling.text)
    else:
        next_volume_dates.append("")
for item in latest_releases_dates:
    if item != "N.D.":
        response_latest = requests.get(item)
        soup_latest = BeautifulSoup(response_latest.text, 'html.parser')
        latest_date_parent = soup_latest.find('strong', text="Data pubblicazione:")
        latest_volume_dates.append(latest_date_parent.next_sibling.text)
    else:
        latest_volume_dates.append("")

dates_new_stripped = []
for date in next_volume_dates:
    dates_new_stripped.append(date.strip())
dates_new_stripped = [x for x in dates_new_stripped if x]

next_releases_stripped = []
for release in next_releases:
    next_releases_stripped.append(release.strip())
next_releases_stripped = [x for x in next_releases_stripped if x]

manga_results = [None]*(len(dates_new_stripped)+len(next_releases_stripped))
manga_results[::2] = dates_new_stripped
manga_results[1::2] = next_releases_stripped

print("Sending message...")
bot.send_message(chat_id=my_tg_chatID, text="\n".join(manga_results))
print("Done.")
quit()

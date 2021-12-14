import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from time import sleep

def send_msg(text):
   token = config.token
   chat_id = config.chatID
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   response = requests.get(url_req)
   print(response.json())
   
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 5)

mangalist = config.mangalist

home_url = "https://www.animeclick.it"
items = []
titles_ita = []
italy_statuses = []
next_releases = []
next_releases_long = []
next_releases_dates = []
latest_releases = []
latest_releases_dates = []

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
        prossima_uscita = soup.find('h3').getText()
        next_releases_long.append(prossima_uscita.strip())
        if 15 <= len(prossima_uscita.strip()) < 20:
            prossima_uscita = prossima_uscita[:7] + "..." + prossima_uscita[10:]
        if 20 <= len(prossima_uscita.strip()) < 30:
            prossima_uscita = prossima_uscita[:12] + "..." + prossima_uscita[18:]
        elif 30 <= len(prossima_uscita.strip()) <= 50:
            prossima_uscita = prossima_uscita[:10] + "..." + prossima_uscita[30:]
        next_releases.append(prossima_uscita.strip())       # NEW
        next_release_link = soup.select_one("a[href*=edizione\/]")
        next_releases_dates.append(home_url+next_release_link.get('href'))
        latest_releases.append("")
        latest_releases_dates.append("N.D.")
    elif target_statoIt.strip() == "completato" and soup.find(text="Prossima uscita") is not None:
        prossima_uscita = soup.find('h3').getText()
        next_releases_long.append(prossima_uscita.strip())
        if 15 <= len(prossima_uscita.strip()) < 20:
            prossima_uscita = prossima_uscita[:7] + "..." + prossima_uscita[10:]
        if 20 <= len(prossima_uscita.strip()) < 30:
            prossima_uscita = prossima_uscita[:12] + "..." + prossima_uscita[18:]
        elif 30 <= len(prossima_uscita.strip()) <= 50:
            prossima_uscita = prossima_uscita[:10] + "..." + prossima_uscita[30:]
        next_releases.append(prossima_uscita.strip())      # RISTAMPA
        next_release_link = soup.select_one("a[href*=edizione\/]")
        next_releases_dates.append(home_url+next_release_link.get('href'))
        latest_releases.append("")
        latest_releases_dates.append("N.D.")
    elif soup.find(text="Ultima uscita") is not None:
        ultima_uscita = soup.find('h3').getText()
        latest_releases.append("Ultima uscita: "+ultima_uscita.strip())
        next_release_link = soup.select_one("a[href*=edizione\/]")
        latest_releases_dates.append(home_url+next_release_link.get('href'))
        next_releases.append("")
        next_releases_long.append("")
        next_releases_dates.append("N.D.")
    else:
        next_releases.append("")
        next_releases_long.append("")
        next_releases_dates.append("N.D.")
        latest_releases.append("")
        latest_releases_dates.append("N.D.")
        continue

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

dates_new = []
for date in next_volume_dates:
    dates_new.append(date.replace('/01/', 'gen').replace('/11/', 'nov').replace('/12/', 'dic'))  

dates_new_stripped = []
for date in dates_new:
    dates_new_stripped.append(date.strip())
dates_new_stripped = [x for x in dates_new_stripped if x]

next_releases_stripped = []
for release in next_releases:
    next_releases_stripped.append(release.strip())
next_releases_stripped = [x for x in next_releases_stripped if x]

result = [None]*(len(dates_new_stripped)+len(next_releases_stripped))
result[::2] = dates_new_stripped
result[1::2] = next_releases_stripped

send_msg(str(result))

driver.stop_client()
driver.close()
driver.quit()

# sleep(28800)        # 8 ore
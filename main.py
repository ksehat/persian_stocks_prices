%%shell
# Ubuntu no longer distributes chromium-browser outside of snap
#
# Proposed solution: https://askubuntu.com/questions/1204571/how-to-install-chromium-without-snap

# Add debian buster
cat > /etc/apt/sources.list.d/debian.list <<'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster.gpg] http://deb.debian.org/debian buster main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster-updates.gpg] http://deb.debian.org/debian buster-updates main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-security-buster.gpg] http://deb.debian.org/debian-security buster/updates main
EOF

# Add keys
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A

apt-key export 77E11517 | gpg --dearmour -o /usr/share/keyrings/debian-buster.gpg
apt-key export 22F3D138 | gpg --dearmour -o /usr/share/keyrings/debian-buster-updates.gpg
apt-key export E562B32A | gpg --dearmour -o /usr/share/keyrings/debian-security-buster.gpg

# Prefer debian repo for chromium* packages only
# Note the double-blank lines between entries
cat > /etc/apt/preferences.d/chromium.pref << 'EOF'
Package: *
Pin: release a=eoan
Pin-Priority: 500


Package: *
Pin: origin "deb.debian.org"
Pin-Priority: 300


Package: chromium*
Pin: origin "deb.debian.org"
Pin-Priority: 700
EOF


!apt-get update
!apt-get install chromium chromium-driver
!pip3 install selenium
!pip install -v 'python-telegram-bot==13.15'

# Above code is for the google colab

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram


def get_prices():
    url: str = ("https://fa.navasan.net/")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('chromedriver',options=options)
    try:
        driver.get(url=url)

        name_list = []
        for elem in driver.find_elements(By.XPATH, '//tbody/tr/th'):
            name_list.append(elem.text)

        price_list = []
        for elem in driver.find_elements(By.XPATH, '//tbody/tr/td[1]'):
            price_list.append(elem.text)

        time_list = []
        for elem in driver.find_elements(By.XPATH, '//tbody/tr/td[3]'):
            time_list.append(elem.text)

        return name_list, price_list, time_list
    except Exception as e:
        print(f'There occured an error in the sepehr_scraper.py. {e}')
        return None, None, None


bot_token = '6182826751:AAEGjmTFCTTaRLCtBnScP7GEjahEtPy7jSI'
bot = telegram.Bot(token=bot_token,)
while True:
  name_list, price_list, time_list = [], [], []
  name_list, price_list, time_list = get_prices()
  for idx, value in enumerate(name_list[:7]):
      print(name_list[idx])
      text = f'{name_list[idx]}\n{price_list[idx]}\n{time_list[idx]}'
      bot.send_message(chat_id='@bazar_lahze', text=text)
      time.sleep(1)
  time.sleep(600)
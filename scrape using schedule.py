import schedule
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

#This version practically scrape the table on the webpage automatically daily using schedule python package
URL = "https://www.tpsgc-pwgsc.gc.ca/cgi-bin/recgen/er.pl?Language=E"
web_content = requests.get(URL)
soup = BeautifulSoup(web_content.content, 'html5lib')


def scrape_exchange():
    child_soup = soup.find_all('h2')
    for a_text in child_soup:
        if 'Exchange Rates as of' in a_text.text:
            # saves each file name same as the date displayed on the website
            filename = a_text.text + ' _.csv'
        else:
            pass
    files = filename
    table = soup.find('table', {'class': 'table table-hover table-bordered'})
    df = pd.DataFrame(columns=['Currency', 'Description', 'Rate'])

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            currency = columns[0].text.strip()
            description = columns[1].text.strip()
            rate = float(columns[2].text.strip())
            df = df.append({'Currency': currency, 'Description': description, 'Rate': rate}, ignore_index=True)
    df.to_csv(files, encoding='utf-8')


schedule.every().monday.at("17:00").do(scrape_exchange)
schedule.every().tuesday.at("17:00").do(scrape_exchange)
schedule.every().wednesday.at("17:00").do(scrape_exchange)
schedule.every().thursday.at("17:00").do(scrape_exchange)
schedule.every().friday.at("17:00").do(scrape_exchange)
schedule.every().saturday.at("17:00").do(scrape_exchange)
schedule.every().sunday.at("17:00").do(scrape_exchange)
while True:
    schedule.run_pending()
    time.sleep(1)

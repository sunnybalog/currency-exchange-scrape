import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from threading import Timer
import pandas as pd

# create timestamp to capture date&time of first run and subsequent run of the script
x = datetime.today()
y = x.replace(day=x.day, hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - x
secs = delta_t.total_seconds()

#unction to run the loop
def scrape_cdn_exchange():
    # url to scrape
    URL = "https://www.tpsgc-pwgsc.gc.ca/cgi-bin/recgen/er.pl?Language=E"
    # send requent to the webpage
    web_content = requests.get(URL)

    soup = BeautifulSoup(web_content.content, 'html5lib')
    # create format for columns
    df = pd.DataFrame(columns=['Currency', 'Description', 'Rate'])

    table = soup.find('table', {'class': 'table table-hover table-bordered'})
    # Loop through the table in the webpage and scrape data row by row
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            currency = columns[0].text.strip()
            description = columns[1].text.strip()
            rate = float(columns[2].text.strip())
            df = df.append({'Currency': currency, 'Description': description, 'Rate': rate}, ignore_index=True)

# create csv file with filename as the date of exchange displayed on the webpage
    child_soup = soup.find_all('h2')
    for a_text in child_soup:
        if 'Exchange Rates as of' in a_text.text:
            filename = a_text.text + '_.csv'

# write data into the file
    df.to_csv(filename, encoding='utf-8')

# print to python console if interested to see few lines of scrape data
    print(df.head())


t = Timer(secs, scrape_cdn_exchange())
t.start()

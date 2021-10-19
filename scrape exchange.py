import requests
from bs4 import BeautifulSoup as bS
import sqlite3
from datetime import date, datetime, timedelta
from threading import Timer

# capture current date and time of startup of the python script
x = datetime.now()
# automatically scrape the webpage for define data at exactly 9AM Local time everyday
y = x.replace(day=x.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - x
secs = delta_t.total_seconds()


def hello_world():
    currency = 'NGN'
    current_date = date.today()
    conn = sqlite3.connect('learn.db')
    c = conn.cursor()

    # next two lines used to create new table, comment them out after creating the table
    # c.execute('''CREATE TABLE real_exchange (current_date DATE, currency TEXT, the_exchange REAL)''')
    # conn.commit()

    url = "https://www.tpsgc-pwgsc.gc.ca/cgi-bin/recgen/er.pl?Language=E"
    r = requests.get(url)
    soup = bS(r.content, 'html.parser')

    paragraphs = soup.find_all('td')
    n = 0
    for p in paragraphs:
        if p.text == currency:
            the_index = n
            the_exchange = float(paragraphs[the_index + 2].text)
            c.execute('''INSERT INTO real_exchange VALUES(?, ?, ?)''', (current_date, currency, the_exchange))
            conn.commit()

            # to display table data in python console, if not comment next two lines out
            for row in c.execute('SELECT * FROM real_exchange ORDER BY current_date'):
                print(row)
        else:
            n = n + 1


t = Timer(secs, hello_world)
t.start()

# query to delete all data with specific rowID
# c.execute('''DELETE from real_exchange where DATE="2021-10-17"''')
# conn.commit()

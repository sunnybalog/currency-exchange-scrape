import requests
from bs4 import BeautifulSoup as bS
import sqlite3
from datetime import date, datetime, timedelta
from threading import Timer


x = datetime.now()
y = x.replace(day=x.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - x
secs = delta_t.total_seconds()


def hello_world():
    current_date = date.today()
    conn = sqlite3.connect('cputest.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE exchanger(date DATE, ngn REAL)''')
    # conn.commit()
    url = "https://www.tpsgc-pwgsc.gc.ca/cgi-bin/recgen/er.pl?Language=E"
    r = requests.get(url)
    soup = bS(r.content, 'html.parser')
    n = 0
    for tag in soup.find_all('td'):
        text_extract = ''.join(tag.findAll(text=True))
        if n == 173:
            NGN = float(text_extract)
        else:
            pass
        n = n + 1
    c.execute('''INSERT INTO exchanger VALUES(?, ?)''', (current_date, NGN))
    conn.commit()
    for row in c.execute('SELECT * FROM exchanger ORDER BY date'):
        # results = c.fetchall()
        # print(results)
        print(row)
    # c.execute('''DELETE FROM exchanger''')
    # conn.commit()


t = Timer(secs, hello_world)
t.start()

# query to delete all data with specific rowID
# c.execute('''DELETE from exchanger where DATE="2021-10-17"''')
# conn.commit()

# create new database table, comment out after creation to avoid error
# c.execute('''CREATE TABLE exchanger(date DATE, ngn REAL)''')
# conn.commit()

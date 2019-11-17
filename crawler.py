#!/usr/bin/env python
from bs4 import BeautifulSoup
import random
import requests
import sqlite3

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

URL_FILE = "./data/top100.list"
try:
    db = sqlite3.connect('data/urldb')
    cursor = db.cursor()
    # Check if table users does not exist and create it
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                      websites(url TEXT PRIMARY KEY, position INTEGER, user_agent TEXT, final_status INTEGER, title TEXT)''')
    db.commit()
    position = 1
    with open(URL_FILE, 'r') as url_file:
        for url in url_file:
            # page = requests.get("http://www.youtube.com")
            url = url.rstrip()
            try:
                user_agent = random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}
                page = requests.get(url, headers=headers, allow_redirects=True)
                print("URL: {}\n".format(page.url))
                soup = BeautifulSoup(page.text, 'html.parser')
                try:
                    title = soup.title.string
                except AttributeError:
                    title = "N/A"
                print("Status: {}\nTitle: {}\n".format(page.status_code, title))
                cursor.execute('''INSERT OR REPLACE INTO websites(url, position, final_status, title, user_agent)
                      VALUES(:url, :position, :final_status, :title, :user_agent)''',
                      {'url':page.url, 'position':position, 'final_status':page.status_code, 'title':title, 'user_agent': user_agent})
            except TimeoutError:
                cursor.execute('''INSERT OR REPLACE INTO websites(url, position, final_status, title, user_agent)
                      VALUES(:url, :position, :final_status, :title, :user_agent)''',
                      {'url':page.url, 'position':position, 'final_status': 408, 'title':"N/A", 'user_agent': user_agent})
            except Exception as ex:
                cursor.execute('''INSERT OR REPLACE INTO websites(url, position, final_status, title, user_agent)
                      VALUES(:url, :position, :final_status, :title, :user_agent)''',
                      {'url':page.url, 'position':position, 'final_status': 500, 'title':"N/A", "user_agent":user_agent})
                
            finally:
                db.commit()

            position += 1
except Exception as e:
    # Roll back any change if something goes wrong
    db.rollback()
    raise e

except KeyboardInterrupt:
    print("Got keyboard interrupt...")

finally:
    db.close()
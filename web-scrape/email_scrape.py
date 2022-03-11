from requests_html import HTMLSession
import re
import time

#array of found emails
emails = []
#arrays of all urls, and urls to scrape
urls = []
to_scrape = []

#set up the html session
session = HTMLSession()

#define our starting URL and email regex.
domain = 'https://www.pvaz.net/'
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

#load a specific URL
def loadURL(url):
    global r
    r = session.get(url)
    r.html.render()

#find any emails on the webpage, add to emails[]
def findEmails():
    global r
    for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
        if re_match.group() not in emails:
            emails.append(re_match.group())

#find all 'pvaz' urls on the webpage, add to urls[] and to_scrape[]
def findURLs():
    global r
    links = r.html.absolute_links
    for link in links:
        if 'pvaz.net' in link:
            if link not in urls:
                urls.append(link)
                to_scrape.append(link)

#find all urls on homepage, then we can expand our search
r = session.get(domain)
r.html.render()
findURLs()

for url in to_scrape:
    to_scrape.remove(url)
    if "pvaz.net/" in url:
        try:
            loadURL(url)
            findURLs()
            findEmails()
            time.sleep(0.5)
        except:
            print("Error with" + str(url) + ". Continuing....")
            continue
    #print(len(urls))
    print(emails)

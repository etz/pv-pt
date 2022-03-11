from requests_html import HTMLSession
import re
import time


#for saving progress of scrape
email_file = open("emails.txt", "r+")
emails = email_file.read().splitlines()
url_file = open("urls.txt", "r+")
urls = url_file.read().splitlines()
to_scrape_file = open("to_scrape.txt", "r+")
to_scrape = to_scrape_file.read().splitlines()

#set up the html session
session = HTMLSession()

#define our starting URL and email regex.
domain = 'https://www.yourdomain.com/'
short_domain = 'yourdomain.com'
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

#load a specific URL
def loadURL(url):
    global r
    r = session.get(url)
    r.html.render()

#find all 'yourdomain.com' emails on the webpage, add to emails[]
def findEmails(url):
    global r
    global emails
    for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
        if re_match.group() not in emails:
            if short_domain in re_match.group():
                emails.append(re_match.group())
                email_file.write(re_match.group() + '\n')
                print("Non-duplicate e-mails found on: " + url)
                print(re_match.group())
    email_file.flush()

#find all 'pvaz' urls on the webpage, add to urls[] and to_scrape[]
def findURLs(url):
    global r
    links = r.html.absolute_links
    for link in links:
        if short_domain in link:
            if link not in urls:
                urls.append(link)
                url_file.write(link + "\n")
                to_scrape.append(link)
    url_file.flush()

if len(to_scrape) == 0:
    r = session.get(domain)
    r.html.render()
    findURLs(domain)
else:
    print("Data loaded.. continuing from last URL")

for url in to_scrape:
    to_scrape.remove(url)
    if short_domain in url:
        try:
            loadURL(url)
            findURLs(url)
            findEmails(url)
            to_scrape_file.seek(0)
            to_scrape_file.truncate()
            to_scrape_file.writelines(s + '\n' for s in to_scrape)
        except Exception as e:
            print(e)
            print("Error with " + str(url) + ". Continuing....")
            continue
    #print(len(urls))
    to_scrape_file.flush()

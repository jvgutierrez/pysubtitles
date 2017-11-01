import json
import logging
import re
import requests
from bs4 import BeautifulSoup

from .cache import cached

BASE_URL = 'http://www.addic7ed.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Referer': 'http://www.addic7ed.com',
}
log = logging.getLogger('pysubtitles.providers.addic7ed')


@cached
def fetch_show_list():
    r = requests.get("{0}/shows.php".format(BASE_URL), headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    shows = {}

    for link in soup.find_all(href=re.compile('^/show/\d+$')):
            if link.string is not None:
                shows[link.string.lower()] = link.get('href')
    return shows


def list_subtitles(show, season, episode, language):
    ret = []
    r = requests.get('{0}/serie/{1}/{2}/{3}/0'.format(BASE_URL, show, season, episode), headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    for row in soup.find_all('td', class_='NewsTitle', colspan='3'):
        text = row.text.split(",")[0]
        if len(row.find_all(title="720/1080")) > 0:
            text += " [HD]"
        if len(row.parent.parent.find_all(title="Hearing Impaired")) > 0:
            text += " [HI]"

        for lang in row.parent.parent.find_all(class_='language'):
            link = lang.parent.find(class_='buttonDownload').get('href')
            if language.lower() in lang.text.lower():
                ret.append({'file': text.strip(), 'lang': lang.text.strip(), 'link': '{0}{1}'.format(BASE_URL, link.strip())})
    return ret


def fetch_subtitle(url):
    r = requests.get(url, headers=HEADERS)
    return r.text

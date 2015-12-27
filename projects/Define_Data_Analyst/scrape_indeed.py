from bs4 import BeautifulSoup
import requests
import codecs
import re

params = {
    'publisher': 7116981571348601,
    'q': "data analyst",
    'l': "",
    'start': 0,
    'limit': 25,
    'latlong': 1,
    'userip': "8.19.92.134",
    'useragent': "Mozilla/5.0%Chrome/47.0.2526.106",
    'v': 2
}

cols = ['jobtitle', 'company', 'city', 'state', 'date', 'snippet', 'url',
        'latitude', 'longitude', 'formattedRelativeTime']


def make_row(tag):
    l = []
    for col in cols:
        c = tag.find(col)
        if c:
            if c.string:
                l.append(re.sub('\|', '', c.string))
            else:
                l.append(' ')
        else:
            l.append(' ')
    return '|'.join(l)


def make_header():
    with codecs.open('indeed_jobs.txt', 'w', encoding='utf-8') as fo:
        head = '|'.join(cols)
        fo.write(head+'\n')


def write_rows(start=0, end=None):
    with codecs.open('indeed_jobs.txt', 'a', encoding='utf-8') as file_out:
        for i in range(start, end):
            params['start'] += 25*i
            r = requests.get('http://api.indeed.com/ads/apisearch?', params)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                for result in soup.results.find_all('result'):
                    row = make_row(result)
                    file_out.write(row+'\n')

make_header()
write_rows(0, 3000)






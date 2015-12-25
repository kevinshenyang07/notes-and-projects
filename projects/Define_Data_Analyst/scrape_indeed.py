webapi = 'http://api.indeed.com/ads/apisearch?publisher=7116981571348601&q=data+analyst&l=&sort=&radius=&st=&jt=&start=0' \
         '&&limit=1000&fromage=&filter=&latlong=1&co=us&chnl=&userip=8.19.92.134&useragent=Mozilla/5.0%Chrome/47.0.2526.106&v=2'

from bs4 import BeautifulSoup
from indeed import IndeedClient

client = IndeedClient(publisher=7116981571348601)
params = {
    'q': "data+analyst",
    'l': "",
    'start': 0,
    'limit': 25,
    'latlong': 1,
    'userip': "8.19.92.134",
    'useragent': "Mozilla/5.0%Chrome/47.0.2526.106"
}

search_response = client.search(**params)

for line in search_response:
    print line
from bs4 import BeautifulSoup
import re

with open("indeed.xml", 'r') as fi:
    soup = BeautifulSoup(fi, 'xml')
    results = soup.results.find_all('result')
    pattern_da = re.compile(r'data|analyst', re.IGNORECASE)
    total = 0
    real = 0
    for result in results:
        total += 1
        if pattern_da.search(result.jobtitle.string):
            real += 1
    print "total: %d", total
    print "real: %d", real
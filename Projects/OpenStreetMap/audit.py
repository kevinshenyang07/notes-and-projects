from bs4 import BeautifulSoup
import re
from collections import defaultdict
from pprint import pprint

osmf = 'austin_texas.osm'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_types = defaultdict(set)
expected = ['Street', "Avenue", "Boulevard", "Drive", "Court", "Place", "Loop"
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Terrace"]

mapping = {"St": "Street", "St.": "Street",
           "Rd": "Road", "Rd.": "Road",
           "Ave": "Avenue", "Ave.": "Avenue"}


def audit_street_type(st_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            st_types[street_type].add(street_name)


def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)


def is_street_name(elem):
    return elem['k'] == 'addr:street'


# audit the data first to develop plan for cleaning
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    soup = BeautifulSoup(osm_file, 'xml')
    for elem in soup.osm.children:
        if elem.name == "node" or elem.name == "way":
            for tag in elem.find_all('tag'):
                if is_street_name(tag):
                    audit_street_type(street_types, tag['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    end = street_type_re.search(name).group()
    if end in mapping.keys():
        name = street_type_re.sub(mapping[end], name)
    return name


def test():
    st_types = audit(osmf)
    pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

if __name__ == '__main__':
    test()



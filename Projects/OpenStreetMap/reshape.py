# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pprint
import re
import codecs
import json

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

fpath1 = 'example.osm'
fpath2 = 'chongqing_china.osm'
fpath3 = 'austin_texas.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

st_tail = re.compile(r'st.?|ave.?|')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def shape_element(element):
    node = {"created": {}, "address": {}}
    if element.name == "node" or element.name == "way":
        node['type'] = element.name
        for k, v in element.attrs.iteritems():
            if v is not None:
                if k in CREATED:
                    node["created"][k] = v
                else:
                    node[k] = v
                ''' since tableau use these two number separately,
                # the lon and lat is going to be keeped
                elif k == "lat" and isfloat(v):
                    node["pos"][0] = float(v)
                elif k == 'lon' and isfloat(v):
                    node["pos"][1] = float(v)
                '''
        if element.tag:
            for tag in element.find_all('tag'):
                k_val = tag['k']
                if problemchars.search(k_val) is None:
                    vals = k_val.split(':')
                    if len(vals) == 1:
                        node[k_val] = tag['v']
                    elif len(vals) == 2:
                        k1 = vals[0]
                        k2 = vals[1]
                        if k1 == 'addr':
                            if k2 == 'street':
                                node["address"][k2] = tag['v']  # need regex
                            else:
                                node["address"][k2] = tag['v']
                        else:
                            node[k1] = {k1: {}}
                            node[k1][k2] = tag['v']
        if element.nd:
            node["node_refs"] = []
            for nd in element.find_all('nd'):
                r_val = nd['ref']
                node["node_refs"].append(r_val)
        if len(node['address']) == 0:
            del node['address']
        if len(node['created']) == 0:
            del node['created']
        return node
    else:
        return None


def process_map(file_in):
    file_out = "{0}.json".format(file_in)
    fi = codecs.open(file_in, 'r')
    soup = BeautifulSoup(fi, 'xml')
    with codecs.open(file_out, "w") as fo:
        for element in soup.osm.children:
            if element.name:
                el = shape_element(element)
                if el:
                    fo.write(json.dumps(el) + "\n")
    fi.close()


def test():
    process_map(fpath3)
    # test for the example.osm
    '''
    pprint.pprint(data)

    correct_first_elem = {
        "id": "261114295",
        "visible": "true",
        "type": "node",
        "pos": [41.9730791, -87.6866303],
        "created": {
            "changeset": "11129782",
            "user": "bbmiller",
            "version": "7",
            "uid": "451048",
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.",
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369",
                                    "2199822370", "2199822284", "2199822281"]
    '''

if __name__ == "__main__":

    test()
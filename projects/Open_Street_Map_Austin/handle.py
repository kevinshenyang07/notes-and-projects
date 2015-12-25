from pprint import pprint
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.osm


def most_frequent(key):
    if isinstance(key, str):
        pipeline = [
            {"$match": {key: {"$exists": 1}}},
            {"$project": {key: 1}},
            {"$group": {"_id": "".join("$"+key),
                        "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return pipeline


def aggregate(pipeline):
    agg = db.austin.aggregate(pipeline)
    res = [e for e in agg]
    return res

streets = aggregate(most_frequent("address.street"))
pprint(streets[:10])

cities = aggregate(most_frequent("address.city"))
pprint(cities[:10])

postcodes = aggregate(most_frequent("address.postcode"))
pprint(postcodes[:10])

amenities = aggregate(most_frequent("amenity"))
pprint(amenities[:10])

pipeline_cuisine = [
    {"$match": {"amenity": {"$exists": 1}, "amenity": "restaurant"}},
    {"$group": {"_id": "$cuisine",
                "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]

cuisines = aggregate(pipeline_cuisine)
pprint(cuisines[:10])



# get the viz
pipeline_recreations = [
    {"$match": {"amenity": {"$exists": 1}}},

    {"$project": {"amenity": 1, "name": 1, "lat": 1, 'lon': 1, "_id": 0}},
]

recreations = aggregate(pipeline_recreations)
pprint(recreations[:10])


def get_val(x):
    if isinstance(x, dict):
        return x.keys()[0]
    else:
        return x


import codecs
with codecs.open('res.csv', 'wb', encoding='utf-8') as fo:
        keys = ['lat', 'amenity', 'lon', 'name']
        fo.write(",".join(keys)+'\n')
        for i in range(len(recreations)-1):
            nested_vals = recreations[i+1].values()
            vals = [get_val(v) for v in nested_vals]
            if len(vals) == 4:
                fo.write(",".join(vals)+'\n')


# top five contributors
pc = [{"$group":{"_id":"$created.user",
				  "count":{"$sum":1 }}},
     {"$sort": {"count": -1}},
     {"$limit": 5}]
contributors = aggregate(pc)
pprint(contributors)

# users that appear for single time
ps = [{"$group":{"_id":"$created.user",
                 "count":{"$sum":1}}},
      {"$group":{"_id":"$count",
                 "num_users":{"$sum":1}}},
      {"$sort":{"_id":1}},
      {"$limit": 1}]
single = aggregate(ps)
pprint(single)
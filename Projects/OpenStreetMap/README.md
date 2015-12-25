

# Exploring OpenStreetMap Austin:
##Data Wrangling with BeautifulSoup and MongoDB
                                                
Map Area: Austin, TX, United States

I love Austin and I choose it, but you can retrieve the original osm file around the world from the official source: 

[https://mapzen.com/data/metro-extracts](https://mapzen.com/data/metro-extracts).                                              

1. [Problems Encountered in the Map
Over-­abbreviated Street Names](#problems)
2. [Data Overview](#overview)
3. [Contributor statistics and Additional Ideas](#ideas)
4. [Conclusion and Back to Visual](#visual)

                                                                                                
### <a name="problems">Problems Encountered in the Map</a>

Even though BeautifulSoup offers .children generator, it seems that the soup need to finish parsing the whole file before doing anything, so for xml files larger than 1gb, .iterparse() in elementtree would be a better choice. The extracted austin_texas.osm took me about 30 minutes to parse into .json file.

austin_texas.osm - 1.4 GB / austin_texas.osm.json - 1.66 GB  
                                                
After initially checking the data quality using audit.py file, I find the situation better than I expected. Except for some abbreviation, the addresses are not misplaced or meaningless. Some of the imperfect street types: st. tr. rd. ste. and so on.

                                                
### <a name="overview">Data Overview</a>

                                                
This section contains basic statistics about the dataset and the MongoDB queries used to gather them.
                                                
Number of documents
                                                
> db.austin.count()  
>> 6981886                                              
                                                
Number of nodes: 
                                                
> db.austin.find({"type":"node"}).count()
>> 6322712
                                                
Number of ways
                                                
> db.austin.find({"type":"way"}).count()
>> 659161
                                                
Number of unique users
                                                
> db.austin.distinct("created.user").length
>> 1029

#### Sort cities by count, descending
                                                
> db.austin.aggregate(
> 
>     [{"$match":{"address.city":{"$exists":1}}}, 
>      {"$group":{"_id":"$address.city", 
>                 "count":{"$sum":1}}}, 
>      {"$sort":{"count":­1}}]
> )

I wrote a script to get the result, but you can directly get it in mongo shell, like this.
                                                
And, the results, edited for readability:
                                                
[{u'_id': u'Austin', u'count': 2883},<br/>
 {u'_id': u'Round Rock', u'count': 83},<br/>
 {u'_id': u'Kyle', u'count': 51},<br/>
 {u'_id': u'Austin, TX', u'count': 50},<br/>
 {u'_id': u'Cedar Park', u'count': 27},<br/>
 {u'_id': u'Buda', u'count': 21},<br/>
 {u'_id': u'Pflugerville', u'count': 12},<br/>
 {u'_id': u'Georgetown', u'count': 9},<br/>
 {u'_id': u'Dripping Springs', u'count': 9},<br/>
 {u'_id': u'West Lake Hills', u'count': 8}]

#### Sort streets by count, descending

[{u'_id': u'North Lamar Boulevard', u'count': 678},<br/>
 {u'_id': u'North Interstate Highway 35 Service Road', u'count': 556},<br/>
 {u'_id': u'Burnet Road', u'count': 553},<br/>
 {u'_id': u'Ranch Road 620', u'count': 490},<br/>
 {u'_id': u'South Congress Avenue', u'count': 484},<br/>
 {u'_id': u'Shoal Creek Boulevard', u'count': 445},<br/>
 {u'_id': u'South 1st Street', u'count': 424},<br/>
 {u'_id': u'Guadalupe Street', u'count': 391},<br/>
 {u'_id': u'Manchaca Road', u'count': 391},<br/>
 {u'_id': u'Cameron Road', u'count': 369}]
 
#### Sort postcode by count, descending
 
 [{u'_id': u'78645', u'count': 10882},<br/>
 {u'_id': u'78734', u'count': 5604},<br/>
 {u'_id': u'78653', u'count': 3543},<br/>
 {u'_id': u'78660', u'count': 3468},<br/>
 {u'_id': u'78669', u'count': 3189},<br/>
 {u'_id': u'78641', u'count': 2860},<br/>
 {u'_id': u'78704', u'count': 2488},<br/>
 {u'_id': u'78746', u'count': 2440},<br/>
 {u'_id': u'78759', u'count': 2072},<br/>
 {u'_id': u'78738', u'count': 1937}]
 
#### Sort amenities by count, descending

[{u'_id': u'parking', u'count': 1964},<br/>
 {u'_id': u'restaurant', u'count': 709},<br/>
 {u'_id': u'waste_basket', u'count': 591},<br/>
 {u'_id': u'school', u'count': 559},<br/>
 {u'_id': u'fast_food', u'count': 539},<br/>
 {u'_id': u'place_of_worship', u'count': 491},<br/>
 {u'_id': u'fuel', u'count': 388},<br/>
 {u'_id': u'bench', u'count': 354},<br/>
 {u'_id': u'shelter', u'count': 231},<br/>
 {u'_id': u'bank', u'count': 168}]

#### Sort cuisines by count, descending

[{u'_id': None, u'count': 367},<br/>
 {u'_id': u'mexican', u'count': 70},<br/>
 {u'_id': u'american', u'count': 32},<br/>
 {u'_id': u'pizza', u'count': 25},<br/>
 {u'_id': u'chinese', u'count': 20},<br/>
 {u'_id': u'italian', u'count': 15},<br/>
 {u'_id': u'regional', u'count': 14},<br/>
 {u'_id': u'indian', u'count': 14},<br/>
 {u'_id': u'sandwich', u'count': 13},<br/>
 {u'_id': u'asian', u'count': 13}]


### <a name="ideas">Contributor statistics</a>

                                                
##### Top Five contributing user
                                               

[{u'_id': u'patisilva_atxbuildings', u'count': 2758510},<br/>
 {u'_id': u'ccjjmartin_atxbuildings', u'count': 1304617},<br/>
 {u'_id': u'ccjjmartin__atxbuildings', u'count': 942173},<br/>
 {u'_id': u'wilsaj_atxbuildings', u'count': 353401},<br/>
 {u'_id': u'jseppi_atxbuildings', u'count': 302062}]
 
 Seems that all of them come from the atxbuilding projects.

                                                
#### Number of users appearing only once (having 1 post)
                                                
> db.austin.aggregate(
> 
> [{"$group":{"_id":"$created.user",
>  				 "count":{"$sum":1}}},
>  {"$group":{"_id":"$count",
> 	 			 "num_users":{"$sum":1}}}, 
>  {"$sort":{"_id":1}},
>  {"$limit":1}]
> )

Number: 214. Quite a small number, which indicates that most of the data are still generated by bots or companies.
                                                
### <a name="visual">Conclusion and Back to Visual</a>                       

After this review of the data I believe it has been well cleaned for the purposes of this exercise. What we need is several good questions and even bigger data to get a better view of the whole story. If we can possibly joing the data with other sources, it would be a very exciting thing to do. As github cannot render tableau pages, I'll just put the link below:

[https://public.tableau.com/views/osm_austin/Sheet1?:embed=y&:display_count=yes&:showTabs=y]
(https://public.tableau.com/views/osm_austin/Sheet1?:embed=y&:display_count=yes&:showTabs=y)
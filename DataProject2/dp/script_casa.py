#!/usr/bin/env python3
import sys
import re
print(sys.argv)
stopwords = {'A','house','in','is', 'with','free','for','renting','rooms','available','and','a','monthly','cost','of','u20ac', 'code','mdaedem'}
result  = [word for word in re.split("\W+",sys.argv[2]) if word.lower() not in stopwords]
print(result)
lon =0
lat = 0
lons = -5.99629
lats = 37.3826
lono = -5.84476
lato = 43.3603
lonv = -0.37739
latv = 39.46975
lonb = 2.16992
latb = 41.3879
lonbil = -2.92344
latbil = 43.257
loni = 1.43238
lati = 38.9089
lonm = -3.70325
latm = 40.4167
if result[1] == 'Sevilla':
    lon = lons
    lat = lats
elif result[1] == 'Valencia':
    lon = lonv
    lat =latv
elif result[1] == 'Oviedo':
    lon = lono
    lat = lato
elif result[1] == 'Barcelona':
    lon = lonb
    lat = latb
elif result[1] == 'Bilbao':
    lon = lonbil
    lat = latbil
elif result[1] == 'Ibiza':
    lon = lono
    lat = lato
elif result[1] == 'Madrid':
    lon = lonm
    lat = latm
else:
    print("New city")
import requests
import json
document = {'tweet_id':sys.argv[1],
            'tweet':sys.argv[2],
            'location':[lon,lat],
            'rooms': result[2],
            'city': result[1],
            'price': result[3],
            'house_id': result[4]}
requestResponse = requests.post('http://34.89.193.203:9200/clean_casa/_doc/',json=document)
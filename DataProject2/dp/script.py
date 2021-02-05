#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
import re
import tweepy
from elasticsearch import Elasticsearch
import requests
import json
es = Elasticsearch('http://34.89.193.203:9200')
# Last Tweet
text = sys.argv[2]
tweetId = sys.argv[1]
stopwords_pe = {'my','name','is','mr','mrs','Jr','mdaedem','salary','yearly','and','i','am','years','old','family','are','members','these','are','my','hobbies'}
resultwords  = [word for word in re.split("\W+",text) if word.lower() not in stopwords_pe]
print(resultwords)

### Procesamiento tweet peticion
#Definimos los datos del DF
Cities = ('Barcelona','Valencia', 'Sevilla', 'Bilbao', 'Oviedo', 'Madrid', 'Ibiza')
Hobbies =['Beach','City', 'Nature', 'Party']
Barcelona = [8, 10, 2, 8]
Valencia = [8, 8, 4, 6]
Sevilla = [0, 7, 2, 5]
Bilbao = [5, 6, 6, 5]
Oviedo = [0, 4, 8, 2]
Madrid = [0, 10, 2, 8]
Ibiza = [10, 2, 8, 10]
cityDF = pd.DataFrame({'Hobbies':Hobbies, 'Barcelona':Barcelona, 'Valencia':Valencia, 'Sevilla':Sevilla, 'Bilbao':Bilbao,
 'Oviedo':Oviedo, 'Madrid':Madrid, 'Ibiza':Ibiza})
lista = []
for i in Cities:
        score = (i,abs(cityDF[i][0]-int(resultwords[7]))+
        abs(cityDF[i][1]-int(resultwords[9]))+
        abs(cityDF[i][2]-int(resultwords[11]))+
        abs(cityDF[i][3]-int(resultwords[13])))
        lista.append(score)
sortedlist = sorted(lista, key= lambda l: l[1])
family = resultwords[5]
budget = (int(resultwords[3])/12)*0.20

# Query
res = 0
t = 0

for i in range(6):
        body = {
          "query": {
            "bool": {
              "must": [
                {
                  "match": {
                    "city": sortedlist[i][0]
                  }
                },
                {
                  "range": {
                    "rooms": {
                      "gte": family
                    }
                  }
                },
                {
                  "range": {
                    "price": {
                      "lte": budget
                    }
                  }
                }
              ]
            }
          }
        }
        res=es.search(index="clean_casa", body= body, size=1)
        for hit in res['hits']['hits']:
            t=hit["_source"]['tweet']
            print(t)
        if t != 0 :
            break

# Tweet Reply
if t==0:
    reply_text = " @dlpexercisepro1 unfortunately we do not have any house that meets your requirements, an agent from Quality Life will contact you as soon as possible"
else:
    stopwords_ma = {'A','house','in','is', 'with','free','for','renting','rooms','available','and','a','monthly','cost','of','code','mdaedem'}
    result_ma  = [word for word in re.split("\W+",t) if word.lower() not in stopwords_ma]
    location = result_ma[1]
    rooms = result_ma[2]
    price= result_ma[3]
    house_id=result_ma[4]
    reply_text= '@dlpexercisepro1 The recommended house is placed in' + ' ' + location + ', ' + 'with a renting price of ' + price + '€ and ' + rooms + ' rooms. ' +
 'The house ID is: '+ house_id
CONSUMER_KEY ="PNHWrDrxCplnkwJLJaLzmoM5o"
CONSUMER_SECRET ="HcHdvxgRVEqyaF9kATnO4X2Ysp2PYojKdS6oSXrOyoBncTiveN"
ACCESS_KEY ="1350776176323792898-tleWsOtY3pLbSGNVGBlIHK6fV1FP3V" 
ACCESS_SECRET ="Lht7ooL8NnqvnfbEDd3urEUFfSN0oc6VtNFwiMfmniMH4"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
#api.update_status(reply_text, tweetId)
# Match en elastic
document = {'casa':t,
            'persona':text}
requestResponse = requests.post('http://elasticsearch:9200/monitoring/_doc/',json=document)
#pprint.pprint(requestResponse.json())#!/usr/bin/env python3
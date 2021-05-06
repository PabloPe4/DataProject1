#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 19:47:48 2021

@author: Rosa
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

import pandas as pd
import pickle
import numpy as np
#import lightgbm as lgb
import matplotlib.pyplot as plt
from numpy import asarray
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

import yfinance as yf
import plotly.graph_objs as go
import datetime
from datetime import date, timedelta


# -------------- FETCHING DATA -----------------

start_date = "2020-01-01"
end_date = date.today()
print(end_date)

data_bit = yf.download(tickers='BTC-USD', start = start_date, end = end_date, interval = '1d')
data_bit.head()

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data_bit.index,
                open=data_bit['Open'],
                high=data_bit['High'],
                low=data_bit['Low'],
                close=data_bit['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='Bitcoin live share price evolution',
    yaxis_title='Bitcoin Price (kUS Dollars)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=6, label="6h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()

# -----------------TWITTER SENTIMENT ANALYSIS -----------------

import time
import tweepy
import re

import plotly.express as px
import plotly.graph_objects as go

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

consumer_key = "9o2kGicQ3XmJAvuJ6CbTmHI8w"
consumer_secret = "axLALYLOwqdEO6I3QMo7admIosO7s5JgzOpbYVQL8RB0uYFJmf"
access_key = "1350776176323792898-KsNaj73Z0cH7BXBQAjBO9vqIvoyeCh"
access_secret = "bMbAA5b7hs8agqi2aGUBVO34Pn6wsB05ziwJBh7T1uEhi"
    
def initialize():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())
    return api
api = initialize()

comp_searches = ("#bitcoin", "#ethereum")

# Array to hold sentiment
sentiments = []

# Iterate through all the comp_searches
for search in comp_searches:
       
    # Bring out the 100 tweets
    comp_tweets = api.search(q=search,lang="en", count=100)
    

    # Loop through the 100 tweets
    for tweet in comp_tweets['statuses']:
      text = tweet["text"]
      date = tweet["created_at"]

      #date = list(tweet)[0]
      #print(date)
        
     # Add each value to the appropriate array
      sentiments.append({"Hashtag":search,
                        "text":text,
                       "Date": date,
                        })

#convert array to dataframe
df = pd.DataFrame.from_dict(sentiments)

#cleaning the tweets
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt
def clean_tweets(tweets):
    #remove twitter Return handles (RT @xxx:)
    tweets = np.vectorize(remove_pattern)(tweets, "RT @[\w]*:") 
    
    #remove twitter handles (@xxx)
    tweets = np.vectorize(remove_pattern)(tweets, "@[\w]*")
    
    #remove URL links (httpxxx)
    tweets = np.vectorize(remove_pattern)(tweets, "https?://[A-Za-z0-9./]*")
    
    #remove special characters, numbers, punctuations (except for #)
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")
    
    return tweets

df['text'] = clean_tweets(df['text'])

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
def word_cloud(wd_list):
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        width=1600,
        height=800,
        random_state=1,
        colormap='jet',
        max_words=80,
        max_font_size=200).generate(all_words)

    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]


    for (word, freq), fontsize, position, orientation, color in wordcloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',  
                       text=word_list
                      )
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig


fig2 = word_cloud(df['text'])


# --------------- DASHBOARD ---------------------


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(children=[
        html.Div(
            children=[
                html.H1(
                    children="FIJI", className="header-right"
                ),
                html.H1(
                    children="\u20BF  Pricing prediction", className="header-title"
                ),
                html.P(
                    children= "The predictability of a time-series data: 1 day, 5 days and 1 month",
                    className="header-description",
                ),
            ],
            className="header",
        ),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        config={"displayModeBar": False},
        className="card",

    
    ),
    dcc.Graph(
        id='example',
        figure=fig2,
        config={"displayModeBar": False},
        className="card2",

    
    )
    

])

if __name__ == '__main__':
    app.run_server(debug=True)
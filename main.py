#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json
import urllib3
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def extract_google_trends():
    http = urllib3.PoolManager()
    url = "https://trends.google.com/trends/hottrends/atom/feed"
    response = http.request("GET", url)
    soup = BeautifulSoup(response.data, "html.parser")
    titles_list = soup.find_all('title')
    titles_list = titles_list[1:]
    
    final_data = []
    for title in titles_list:
        title = str(title)[7:len(title)-9]
        final_data.append(title)
    final_data = final_data[:10]
    return final_data
    

trends = extract_google_trends()
#Twitter auth keys
consumer_key = 'f9EJR0KFbYLQMSqLkAF1Z4vxq'
consumer_secret = 'A2xb0oorAztFinBdKx9L6QZKplfWhjpG2bxFuhDCciH6UJjHcU'

access_token = '882553583144718336-RnmjWW5kRXU9pzGErpVrnm1I9ESnH4s'
access_token_secret = 'gjGJpddefqCpLO51pXGGpLrox8gZvE0ek3pIoMXcoztra'

#Authenticating to Twitter
oauth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter = Twitter(auth = oauth)
trend_polarities = {}

#Calculating the total polarity for each trend
for trend in trends:
    public_tweets = twitter.search.tweets(q=trend, count = 100)['statuses']
    #print(twitter.search.tweets(q="curling")['statuses'][3]['text'])
    polarity_sum = 0
    for tweet in public_tweets:
        tweet_text = tweet['text']
        analysis = TextBlob(tweet_text)
        polarity_sum += analysis.polarity
    trend_polarities[trend] = polarity_sum

#Plotting the data
size = [abs(polarity) * 100 for polarity in trend_polarities.values()]
colors = []
for polarity in trend_polarities.values():
    if polarity > 0:
        colors.append((1.0, 0.0, 0.0))
    else:
        colors.append((0.0, 0.0, 1.0))

x = [1,2,3,4,5,6,7,8,9,10]
y = [10, 13, 11, 13, 15, 9, 8, 11, 12, 9]
plt.scatter(x, y, s=size, c=colors, alpha=1)
for i in range(10):
    plt.annotate(list(trend_polarities.keys())[i], xy = (x[i], y[i]))
plt.axis("off")
plt.show()

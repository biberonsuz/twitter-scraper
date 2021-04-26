#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import json
import os
import wget

# load Twitter API credentials

with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)

consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']

# Create the api endpoint

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

# Maximum number of tweets shown per page (max=100)

tweets_per_page = 100

# Number of pages to search in
page_amount = 10

# Hashtag to search for

hashtag = 'teargas'
no_media_tweets = 0

if not os.path.exists(hashtag):
    os.makedirs(hashtag)
    
counter =0;

for tweet in tweepy.Cursor(api.search, q='#' + hashtag, include_entities=True, tweet_mode='extended').items():
	# Get tweets as json objects
	if 'media' in tweet.entities:
		no_media_tweets += 1
		for image in tweet.entities['media']:
	 		wget.download(image['media_url'], out = hashtag)

	#if 'urls' in tweet.entities:
	#	for url in tweet.entities['urls']:
	#		with open('tweet_urls' + hashtag + '.txt', 'a') as the_file:
	# 			the_file.write(str(url['url'].encode('utf-8')) + '\n')
		counter+=1
		txtfile = image['media_url'].split( '/' ).pop( )
		with open(hashtag + '/' + txtfile + '.' + str(counter) + '.txt', 'a') as the_file:
			the_file.write(str(tweet.full_text) + '\n')
			#utf / txt issue with non latin characters and emojis. Probably bit difference?

	#extracting as JSON, or JS objects. 
	#name the image file with an id of the tweet.

print(f'Extracted {tweets_per_page * page_amount} tweets with hashtag #{hashtag}', f'{no_media_tweets} tweets found that contain media.')

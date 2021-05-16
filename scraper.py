#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import json
import os
import wget
from googletrans import Translator

translator = Translator(service_urls=['translate.googleapis.com'])

# load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)

consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_token = info['ACCESS_TOKEN']
access_secret = info['ACCESS_TOKEN_SECRET']

# Create the api endpoint
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

# Hashtag to search for
hashtag = 'teargas'

if not os.path.exists(hashtag):
    os.makedirs(hashtag)
    
def scrape(lang):
	result = translator.translate(hashtag, dest=language)
	translated = result.text

	counter =0;

	for tweet in tweepy.Cursor(api.search, q='#' + translated, include_entities=True, tweet_mode='extended').items():
		# Get tweets as json objects
		if 'media' in tweet.entities:
			#for image in tweet.entities['media']:
		 		#wget.download(image['media_url'], out = hashtag)

			counter+=1
			txtfile = image['media_url'].split( '/' ).pop( )
			print(tweet.full_text)
			#with open(hashtag + '/' + txtfile + '.' + str(counter) + '.txt', 'a') as the_file:
				#the_file.write(str(tweet.full_text) + '\n')


print(f'Extracted {counter} tweets with hashtag #{hashtag} in {lang}.')

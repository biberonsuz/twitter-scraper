#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import tweepy
import json
import os
import wget
from textblob import TextBlob
#from googletrans import Translator

#translator = Translator(service_urls=['translate.googleapis.co.kr', 'translate.googleapis.com'])

languages = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'he']

# load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)

consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_token = info['ACCESS_TOKEN']
access_secret = info['ACCESS_TOKEN_SECRET']

# Create the api endpoint
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Hashtag to search for
hashtag = 'teargas'

#define array for translating the hashtag
translated_queries = []

#define array for getting similar hashtags


if not os.path.exists(hashtag):
    os.makedirs(hashtag)
 
def translate_query(lang):
	translated = TextBlob(hashtag).translate(to=lang)#.replace(" ", "")

	translated_queries.append(translated)
	print(lang, translated)

#less precise, more content
def search_for_similar_hash(query): 
	similar_hashtags = []

	for tweet in tweepy.Cursor(api.search, q='#' + str(query), include_entities=True, tweet_mode='extended').items():
		if 'media' in tweet.entities:
			similar_hash = tweet.entities['hashtags']
			for a in similar_hash:
				similar_hashtags.append(a.get('text'))

	if len(similar_hashtags) != 0:
		for h in similar_hashtags:
			scrape(h)
	
def scrape(query):
	print(f'Searching for {query}...')

	extract_counter =0
	found_counter =0
	tweet_lang = ''

	for tweet in tweepy.Cursor(api.search, q=query, include_entities=True, tweet_mode='extended').items():
		# Get tweets as json objects
		
		if 'media' in tweet.entities:
			tweet_lang = tweet.lang
			found_counter+=1
			if not os.path.exists(f'{hashtag}/{tweet_lang}'):
				os.makedirs(f'{hashtag}/{tweet_lang}')

			for image in tweet.extended_entities['media']:
				fileName = image['media_url'].split( '/' ).pop( )
				if not os.path.exists(f'{hashtag}/{tweet_lang}/{fileName}'):
					extract_counter+=1
					wget.download(image['media_url'], out = f'{hashtag}/{tweet_lang}')
					print(f'\n Downloaded {extract_counter} images.')

					with open(f'{hashtag}/{tweet_lang}/{fileName}.txt', 'a') as the_file:
						the_file.write(str(tweet.full_text) + '\n')
						if tweet_lang != 'en' or 'und':
							translated_tweet = TextBlob(tweet.full_text).translate(to='en')
							the_file.write('\n' + str(translated_tweet) + '\n')
				else:
					print(f'Found {found_counter} already downloaded tweets.')

	print(f'Found {found_counter} tweets, extracted {extract_counter} tweets with hashtag {query} in language {tweet_lang}.')

# for l in languages:
# 	translate_query(l)

# with open(f'{hashtag}/translated-queries-{hashtag}.json', 'w') as outfile:
# 	json.dump(translated_queries, outfile, ensure_ascii=False)

with open(f'{hashtag}/translated-queries-{hashtag}.json') as query_data:
	queries = json.load(query_data)

for q in queries[99:]:
	#search as hashtag
	#q_hashtag = q.replace(" ", "")
	#scrape(f'#{q_hashtag}')

	#search as words
	scrape(q)


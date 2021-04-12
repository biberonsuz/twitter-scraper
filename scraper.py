import tweepy
import json
import os
import wget
#req googletrans-3.1.0a0
from googletrans import Translator
import datetime

# load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)

consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']

# Create the Tweepy api endpoint
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

#load events.json for events, dates, locations etc.
with open('events.json') as events_json:
	events = json.load(events_json)

#set translator for Google API.
translator = Translator(service_urls=['translate.googleapis.com'])

def scrape(hashtag, language, date):
	result = translator.translate(hashtag, dest=language)
	translated = result.text

	no_media_tweets = 0

	print(date)

	for tweet in tweepy.Cursor(api.search, q='#' + translated, lang=language, since=date, include_entities=True, tweet_mode='extended').items():
		# Get tweets as json objects
		if 'media' in tweet.entities:
			no_media_tweets += 1
			for image in tweet.entities['media']:
	 			wget.download(image['media_url'], out = hashtag)

		with open('tweets_with_hashtag_' + hashtag + '.txt', 'a') as the_file:
	 		the_file.write(str(tweet.full_text.encode('utf-8')) + '\n')
	 		#toEng=Translator(from_lang= 'ar', to_lang='en')
			#translationEng = toEng.translate(translationLang)
	 		#utf / txt issue with non latin characters and emojis. Probably bit difference?

	print(f'Extracted tweets with hashtag #{hashtag} ({translationLang})', f'{no_media_tweets} tweets found that contain media.')

# Hashtag/s to search for
hashtag = 'teargas'

translator = Translator(service_urls=['translate.googleapis.com'])
result = translator.translate(hashtag, dest='ar')
print(result.text)

# Make a directory for hashtag
if not os.path.exists(hashtag):
    os.makedirs(hashtag)

# Get Language and Date from events.json
for i in range(len(events)):
	lang_str = events[i]['Language']
	date_str = events[i]['Date']

	# take the first date, if there the event is between two dates.
	if isinstance(date_str, list):
		print(date_str)
		if isinstance(lang_str, list):
			scrape(hashtag, lang_str[0], date)
			scrape(hashtag, lang_str[1], date)
		else:
			scrape(hashtag, lang_str, date)
	else:
		date = date_str
		if isinstance(lang_str, list):
			scrape(hashtag, lang_str[0], date)
			scrape(hashtag, lang_str[1], date)
		else:
			scrape(hashtag, lang_str, date)

	



	




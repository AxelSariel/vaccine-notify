import json
import tweepy
import config
import time
import datetime
from apns import APNs, PayloadAlert, Payload

# Twitter API Keys
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
words_all = config.words_all # Words to be matched first
words_any = config.words_any # Words to be matched second
tokens = config.tokens # Device notification tokens to send notifications to
vaccine_bot_username = config.vaccine_bot_username # Twitter Username to get vaccine tweets from


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
lastTweetID = None

def getNewTweets(since):
	print('\n\n----- ----- CHECKING FOR NEW TWEETS - ' + str(datetime.datetime.now()) + ' ----- -----\n')
	print('Since: '+ str(since))
	tweets = api.user_timeline(vaccine_bot_username, since_id=since, count=100)

	tweetsJsons = []
	for tweet in tweets:
		tweetsJsons.append(tweet._json)

	ids = []
	for tweet in tweetsJsons:
		ids.append(tweet['id'])

	if len(ids)>0:
		global lastTweetID
		lastTweetID = max(ids)
		print('Received ' + str(len(ids)) + ' tweets.')
		print('Last tweet ID: ' + str(lastTweetID))
		processTweets(tweetsJsons)
	else:
		print('Didn\'t receive any new tweets.')

	
def processTweets(jsonList):
	matchedRequired = []
	for tweet in jsonList:
		if any(word.lower() in tweet['text'].lower() for word in words_all):
			tweetObject = {
				'id' : tweet['id'],
				'text' : tweet['text'],
				'url' : tweet['entities']['urls'][0]['url']
			}
			matchedRequired.append(tweetObject)

	matchedTweets = []
	for tweet in matchedRequired:
		if any(word.lower() in tweet['text'].lower() for word in words_any):
			matchedTweets.append(tweet)

	# print('Found ' + str(len(matchedRequired)) + ' tweets matching the requireds.')
	# print(json.dumps(matchedRequired, indent=4))

	print('Found ' + str(len(matchedTweets)) + ' tweets matching anys.')
	print(json.dumps(matchedTweets, indent=4))

	if len(matchedTweets) > 0:
		sendNotification(matchedTweets)

def sendNotification(tweetList):
	for tweet in tweetList:
		print('\n\n<> <> <> <> <> SENDING NOTIFICATION <> <> <> <> <>\n')
		print(tweet['text'])
		print(tweet['url'])
		send_notification('Tweet Matched!', '', tweet['text'])
		print('\n')

def send_notification(title, subtitle, message):
	apns = APNs(use_sandbox=True, cert_file='cert_file.pem',
					key_file='key_file.pem')
	alert = PayloadAlert(title=title, subtitle=subtitle, body=message)
	payload = Payload(alert=alert, sound='default')
	for token in tokens:
		apns.gateway_server.send_notification(token, payload)


while True:
	getNewTweets(lastTweetID)
	time.sleep(15)
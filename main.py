import tweepy
import re

def extractReadable(text):
    print(text)
    if isBunny(text):
        # the bunnies always have the same unicode characters (and patterns) in
        # them, so we can do a little fancy matching to just strip away all the
        # lines we don't want
        text = [
            line for line in text.split('\n')
            if not bool(re.search('[￣＿ㅅづ]+|\/\)+', line))
        ]
        text = [line.strip() for line in text if line != '']
        return ' '.join(text)
    else:
        print("input not recognized as a bunny holding a sign")
        return None

def isBunny(text):
    return "(•ㅅ•)" in text

def getBody(tweet):
    if hasattr(tweet, 'full_text'):
        return tweet.full_text
    else:
        return tweet.text

#replace with your oauth credentials
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

def respond(tweet):
    parent = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
    text = getBody(parent)
    if parent is None:
        print("parentless")
        tweet = api.get_status(tweet.id, tweet_mode="extended").full_text
        text = getBody(tweet)
    text = extractReadable(text)
    if text is not None:
        username = tweet.user.screen_name
        print(username)
        text = '@' + username + ' ' + text
        print(text)
        api.update_status(text, in_reply_to_status_id = tweet.id)

import tweepy
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        respond(status)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['bunnyaccess'])

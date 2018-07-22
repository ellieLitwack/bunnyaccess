import re

import tweepy

from config import ACCESS_TOKEN_KEY
from config import ACCESS_TOKEN_SECRET
from config import OAUTH_CONSUMER_SECRET
from config import OAUTH_CONSUMER_TOKEN
from config import WATCH_WORD

def clean_text(text):
    # First things first: make sure everything's actually in ASCII so that
    # we can work with it
    full_to_half = str.maketrans(
        '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥ'
        'ＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！，゛－＃＄％＆（）＊＋、ー。．／：；'
        '〈＝〉？＠［］＾＿‘｛｜｝～　＇',
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!,"-'
        '#$%&()*+,-../:;<=>?@[]^_`{|}~ \'',
    )
    cleaned_text = ''

    for c in text:
        try:
            c = chr(full_to_half[ord(c)])
        except KeyError:
            pass
        cleaned_text += c

    return cleaned_text

def extractReadable(text):
    print(text)
    if isBunny(text):
        text = clean_text(text)
        # the bunnies always have the same unicode characters (and patterns) in
        # them, so we can do a little fancy matching to just strip away all the
        # lines we don't want
        text = [
            line for line in text.split('\n')
            if not bool(re.search('[￣＿❀ㅅづ]+|\/\)+', line))
        ]
        # strip out extra detritus
        text = [
            line.strip().strip('|').strip() for line in text
            if line.strip() != '' and
               not bool(re.search('^\|[_]+\|$', line.strip()))
        ]
        # Sometimes words are hyphenated; then the join adds an extra space. Let's
        # fix that as we return the string.
        return re.sub(r'- ', '-', ' '.join(text))
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

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        respond(status)

if __name__ == "__main__":
    # all of this information should be handled in config.ini
    auth = tweepy.OAuthHandler(OAUTH_CONSUMER_TOKEN, OAUTH_CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=[WATCH_WORD])

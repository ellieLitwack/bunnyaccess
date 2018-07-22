import configparser
import os

if not os.path.exists('./config.ini'):
    raise Exception('Must have config.ini configured and in the same directory!')

c = configparser.ConfigParser()
c.read('./config.ini')

twitter = c['twitter']
main = c['main']

OAUTH_CONSUMER_TOKEN = twitter['oauth_consumer_token']
OAUTH_CONSUMER_SECRET = twitter['oauth_consumer_secret']

ACCESS_TOKEN_KEY = twitter['access_token_key']
ACCESS_TOKEN_SECRET = twitter['access_token_secret']

WATCH_WORD = main['watch_word']

import tweepy
import config as c
import json

class stream_listener(tweepy.StreamListener):  
    def on_data(self, data):
        tweet = json.loads(data)
        print tweet['text']

auth = tweepy.OAuthHandler(c.c_key, c.c_secret)
auth.set_access_token(c.a_key, c.a_secret)

twitter_stream = tweepy.Stream(auth, stream_listener())

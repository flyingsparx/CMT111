import tweepy
import config as c

class stream_listener(tweepy.StreamListener):  
    def on_status(self, status):
        print status.text

auth = tweepy.OAuthHandler(c.c_key, c.c_secret)
auth.set_access_token(c.a_key, c.a_secret)

twitter_stream = tweepy.Stream(auth, stream_listener())

twitter_stream.filter(locations=[-122.75,36.8,-121.75,37.8])

# This answers most of problem 3 on the practical slides.

import tweepy
import config as c
import random

import json

auth = tweepy.OAuthHandler(c.c_key, c.c_secret)
auth.set_access_token(c.a_key, c.a_secret)

class MyModelParser(tweepy.parsers.ModelParser):
    def parse(self, method, payload):
        result = super(MyModelParser, self).parse(method, payload)
        result._payload = json.loads(payload)
        result.json = payload
        return result

api = tweepy.API(auth)#parser=MyModelParser())


start_user = api.get_user("flyingsparx")
followers = start_user.followers(count=100)

 


for i in range(10):
    random_follower = None
    while random_follower is None or random_follower.protected:
        random_follower = followers[random.randint(0, len(followers)-1)]
    results = api.user_timeline(screen_name=random_follower.screen_name, count=100)
    for r in results:
        print(json.dumps(r._json))


 

#results = api.user_timeline(screen_name='twitter')


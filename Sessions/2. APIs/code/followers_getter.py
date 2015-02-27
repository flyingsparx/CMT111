# This answers most of problem 2 on the practical slides.
#
# This doesn't bother getting the tweets or followers, but
# the logic should be obvious. 
#
# Prints the current user at each stage.

import tweepy
import config as c
import random

auth = tweepy.OAuthHandler(c.c_key, c.c_secret)
auth.set_access_token(c.a_key, c.a_secret)
api = tweepy.API(auth)

def get_random_follower_of_user(user):
    found = False
    follower = None
    while not found:
        try:
            followers = user.followers()
            follower = followers[random.randint(0, len(followers)-1)]
            found = True
        except Exception as e:
            print e
    return follower

current_user = api.get_user("flyingsparx")
users = []

for i in range(10):
    users.append(current_user)
    new_user = get_random_follower_of_user(current_user)
    print new_user.screen_name
    current_user = new_user

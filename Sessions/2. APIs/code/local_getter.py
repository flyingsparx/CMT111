# This answers most of problem 3 on the practical slides.

import tweepy
import config as c
import networkx as nx
import matplotlib.pyplot as plt
import random

auth = tweepy.OAuthHandler(c.c_key, c.c_secret)
auth.set_access_token(c.a_key, c.a_secret)
api = tweepy.API(auth)

start_user = api.get_user("flyingsparx")
followers = start_user.followers(count=70)

G = nx.DiGraph()
G.add_node(start_user)

for i, follower in enumerate(followers):
    G.add_edge(follower, start_user)

for i in range(3):
    random_follower = None
    while random_follower is None or random_follower.protected:
        random_follower = followers[random.randint(0, len(followers)-1)]

    followers2 = random_follower.followers(count=20)
    for follower2 in followers2:
        G.add_edge(follower2, random_follower)

nx.draw(G)
plt.plot()
plt.show()

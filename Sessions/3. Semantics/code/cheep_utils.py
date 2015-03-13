# Utility classes for creating a Twitter-like social network.
#
# See docs on GitHub for more information.

import sqlite3, urllib2, urllib, json

class Cheep:
    def __init__(self, id=None,text=None,user=None, sentiment=None):
        if id is None or text is None or user is None:
            raise Exception("Required info for construcing Cheep: id, text, user.")
        self.id = id
        self.text = text
        self.user = user
        self.sentiment = "UNKNOWN"
    def __str__(self):
        return "Cheep "+str(self.id)+" [user: "+str(self.user)+"] [text: "+str(self.text)+"]"
    def __repr__(self):
        return self.__str__()

class SentimentAnalyser:
    def __init__(self, api_key = None):
        self.api_key = api_key
    def get_cheep_sentiment(self, cheep):
        if self.api_key is None or self.api_key == "":
            raise Exception("Initialise class with your API key first.")
        url = "http://api.datumbox.com/1.0/TwitterSentimentAnalysis.json"
        data = {'api_key':self.api_key, 'text':cheep.text}
        encoded_data = urllib.urlencode(data)
        request = urllib2.Request(url, encoded_data)
        response = json.loads(urllib2.urlopen(request).read())
        if response['output']['status'] == 1:
            return response['output']['result']
        else:
            raise Exception("Could not fetch sentiment for given cheep.")

class CheepEngine:
    def __init__(self):
        self._con = None
        self._create_tables()

    def _connect(self):
        if self._con is None:
            # check_same_thread=False is NOT generally recommended!
            self._con = sqlite3.connect("cheep_base.db", check_same_thread = False)
        self._c = self._con.cursor()

    def _create_tables(self):
        self._connect()
        self._c.execute("CREATE TABLE IF NOT EXISTS cheep (id NUMBER, user TEXT, text TEXT, sentiment TEXT)")
        self._c.execute("CREATE TABLE IF NOT EXISTS follower(user TEXT, follower TEXT)")
        self._c.execute("CREATE TABLE IF NOT EXISTS user(name TEXT)")
        self._con.commit()

    def reset(self):
        self._connect()
        self._c.execute("DROP TABLE cheep")
        self._c.execute("DROP TABLE follower")
        self._c.execute("DROP TABLE user")
        self._create_tables()

    def create_user(self, name):
        self._connect()
        if self.get_user(name) is None:
            self._c.execute("INSERT INTO user VALUES('"+name+"')")
            self._con.commit()
        else:
            raise Exception("User with name "+str(name)+" already exists!")

    def get_user(self, name):
        self._connect()
        user = self._c.execute("SELECT * FROM user WHERE name='"+name+"'").fetchone()
        if user is None:
            return None
        return user[0]

    def get_users(self):
        self._connect()
        users = []
        for u in self._c.execute("SELECT * FROM user").fetchall():
            users.append(u[0])
        return users

    def delete_user(self, name):
        self._connect()
        self._c.execute("DELETE FROM user WHERE name='"+name+"'")
        self._con.commit()

    def add_follower(self, user, follower):
        self._connect()
        if self.get_user(user) is None or self.get_user(follower) is None:
            raise Exception("Either/both users do not exist.")
        user_data = (user, follower)
        self._c.execute("DELETE FROM follower WHERE user='"+user+"' and follower='"+follower+"'")
        self._c.execute("INSERT INTO follower VALUES(?,?)", user_data)
        self._con.commit()
    
    def delete_follower(self, user, follower):
        self._connect()
        if self.get_user(user) is None or self.get_user(follower) is None:
            raise Exception("Either/both users do not exist.")
        self._c.execute("DELETE FROM follower WHERE user='"+user+"' and follower='"+follower+"'")
        self._con.commit()

    def get_followers(self, user):
        self._connect()
        followers = []
        for f in self._c.execute("SELECT follower FROM follower WHERE user='"+user+"'").fetchall():
            followers.append(f[0])
        return followers

    def get_friends(self, user):
        self._connect()
        friends = []
        for f in self._c.execute("SELECT user FROM follower WHERE follower='"+user+"'").fetchall():
            friends.append(f[0])
        return friends 

    def _get_followships(self):
        self._connect()
        followships = []
        for f in self._c.execute("SELECT * FROM follower").fetchall():
            followships.append(f)
        return followships

    def add_cheep(self, cheep):
        self._connect()
        if self.get_cheep_by_id(cheep.id) is not None:
            raise Exception("There's already a cheep with that ID!")
        if self.get_user(cheep.user) is None:
            raise Exception("There is no registered user with name "+str(cheep.user))
        cheep_data = (cheep.id, cheep.user, cheep.text, cheep.sentiment)
        self._c.execute("INSERT INTO cheep VALUES (?,?,?,?)", cheep_data)
        self._con.commit()

    def get_cheep_by_id(self, id):
        self._connect()
        c = self._c.execute("SELECT * FROM cheep WHERE id="+str(id)).fetchone()
        if c is None:
            return None
        return Cheep(c[0], c[2], c[1], c[3])

    def get_cheeps(self):
        self._connect()
        cheeps = []
        for c in self._c.execute("SELECT * FROM cheep").fetchall():
            cheeps.append(Cheep(c[0], c[2], c[1], c[3]))
        return cheeps

    def get_cheeps_by_sentiment(self, sentiment):
        self._connect()
        cheeps = []
        for c in self._c.execute("SELECT * FROM cheep WHERE sentiment='"+str(sentiment)+"'").fetchall():
            cheeps.append(Cheep(c[0], c[2], c[1], c[3]))
        return cheeps

    def get_cheeps_of_user(self, user):
        self._connect()
        if self.get_user(user) is None:
             raise Exception("There is no registered user with name "+str(user))
        cheeps = []
        for c in self._c.execute("SELECT * FROM cheep WHERE user='"+user+"'").fetchall():
            cheeps.append(Cheep(c[0], c[2], c[1], c[3]))
        return cheeps

    def get_cheeps_of_friends(self, user):
        self._connect()
        if self.get_user(user) is None:
             raise Exception("There is no registered user with name "+str(user))
        cheeps = []
        for c in self._c.execute("SELECT c.id, c.user, c.text, c.sentiment FROM cheep as c LEFT JOIN follower as f on c.user=f.user WHERE f.follower='"+user+"'").fetchall():
            cheeps.append(Cheep(c[0], c[2], c[1], c[3]))
        return cheeps

    def delete_cheep(self, id):
        self._connect()
        self._c.execute("DELETE FROM cheep WHERE id="+str(id))
        self._con.commit()

    def get_social_graph(self):
        import networkx as nx
        G = nx.DiGraph()
        for user in self.get_users():
            G.add_node(user)
        for f in self._get_followships():
            G.add_edge(f[1], f[0])
        return G

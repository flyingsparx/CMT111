import sqlite3, urllib2, urllib, json

class Cheep:
    def __init__(self, id=None,text=None,user=None,sentiment=None):
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

class CheepNetwork:
    def __init__(self):
        self.con = sqlite3.connect("cheep_base.db")
        self.c = self.con.cursor()
        self._create_tables()

    def _create_tables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS cheep (id NUMBER, user TEXT, text TEXT, sentiment TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS follower(user TEXT, follower TEXT)")
        self.con.commit()

    def reset(self):
        self.c.execute("DROP TABLE cheep")
        self.c.execute("DROP TABLE follower")
        self._create_tables()

    def add_follower(self, user, follower):
        user_data = (user, follower)
        self.c.execute("DELETE FROM follower WHERE user='"+user+"' and follower='"+follower+"'")
        self.c.execute("INSERT INTO follower VALUES(?,?)", user_data)
        self.con.commit()
    
    def delete_follower(self, user, follower):
        self.c.execute("DELETE FROM follower WHERE user='"+user+"' and follower='"+follower+"'")
        self.con.commit()

    def get_followers(self, user):
        followers = []
        for f in self.c.execute("SELECT follower FROM follower WHERE user='"+user+"'").fetchall():
            followers.append(f[0])
        return followers

    def get_friends(self, user):
        friends = []
        for f in self.c.execute("SELECT user FROM follower WHERE follower='"+user+"'").fetchall():
            friends.append(f[0])
        return friends 

    def add_cheep(self, cheep):
        if self.get_cheep_by_id(cheep.id) is not None:
            raise Exception("There's already a cheep with that ID!")
        cheep_data = (cheep.id, cheep.user, cheep.text, cheep.sentiment)
        self.c.execute("INSERT INTO cheep VALUES (?,?,?,?)", cheep_data)
        self.con.commit()

    def get_cheep_by_id(self, id):
        cheep_data = self.c.execute("SELECT * FROM cheep WHERE id="+str(id)).fetchone()
        if cheep_data is None:
            return None
        return Cheep(cheep_data[0], cheep_data[2], cheep_data[1], cheep_data[3])

    def get_cheeps_by_sentiment(self, sentiment):
        cheeps = []
        for c in self.c.execute("SELECT * FROM cheep WHERE sentiment="+str(sentiment)).fetchall():
            cheeps.append(Cheep(cheep_data[0], cheep_data[2], cheep_data[1], cheep_data[3]))
        return cheeps

    def get_cheeps_of_user(self, user):
        cheeps = []
        for c in self.c.execute("SELECT * FROM cheep WHERE user='"+user+"'").fetchall():
            cheeps.append(Cheep(c[0], c[2], c[1], c[3]))
        return cheeps

    def get_cheeps_of_friends(self, user):
        cheeps = []
        for c in self.c.execute("SELECT c.id, c.user, c.text, c.sentiment FROM cheep as c LEFT JOIN follower as f on c.user=f.user WHERE f.follower='"+user+"'").fetchall():
            cheeps.append(Cheep(c[0], c[2], c[1], c[3]))
        return cheeps

    def delete_cheep(self, id):
        self.c.execute("DELETE FROM cheep WHERE id="+str(id))
        self.con.commit()

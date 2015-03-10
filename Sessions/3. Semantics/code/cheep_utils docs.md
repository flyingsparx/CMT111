# Documentation for `cheep_utils`

This module supports some server-side functionality for creating a Twitter clone. The module has functionality for:

* Creating and modifying a simple directed social graph
* Creating, accessing, and deleting cheeps
* Retrieving cheep sentiment using DatumBox

## Classes

You can import all three classes as you would with any Python module:

`from cheep_utils import Cheep, SentimentAnalyser, CheepNetwork`

### `Cheep(id = None, user = None, text = None, sentiment = None)`

This class represents an individual cheep. Printing a `Cheep` instance results in useful output describing the object.

Throws an `Exception` if ID, user, or text not supplied.

#### Example usage

```python
cheep = Cheep(1, 'will', 'Cheep content!')
print cheep # [Cheep 1 [user: will] [text: Cheep content!]
```

### `SentimentAnalyser(api_key = None)`

This class supports the retrieval of a `Cheep` instance's sentiment using the DatumBox API.

#### Method details

##### `str get_cheep_sentiment(Cheep)`

Accepts a `Cheep` instance and returns a `str` representation of the instance's sentiment.

Throws an `Exception` if class not instantiated with a DatumBox API key.

#### Example usage

```python
cheep = Cheep(1, 'will', 'Cheep content!')
s = SentimentAnalyser("API_KEY")
sentiment = s.get_cheep_sentiment(cheep)
```

### `CheepNetwork()`

This class represents a Cheep network. It persists all data (users, followers, cheeps, sentiment) through `sqlite3`.

All users should be represented by Strings (e.g. `"will"`) and all cheep IDs should be integers (e.g. `1`).

#### Method details

##### `add_follower(user, follower)`

Adds `followe` to `user`'s followers list.

##### `delete_follower(user, follower)`

Removes `follower` from `user`'s followers list.

##### `str[] get_followers(user)`

Returns a list of followers of `user`.

##### `str[] get_friends(user)`

Returns a list of the friends of `user`. *(Note: Friends are the inverse of followers)*

##### `add_cheep(Cheep)`

Adds a new instantiated `Cheep` object to the network.

Throws an exception if a cheep with the same ID already exists.

##### `Cheep get_cheep_by_id(id)`

Returns a single `Cheep` instance with ID matching `id`.

#### `Cheep[] get_cheeps()`

Returns a list of all `Cheep` instances in the network.

##### `Cheep[] get_cheeps_by_sentiment(sentiment)`

Returns a list of `Cheep` instances with sentiment `sentiment`.

##### `Cheep[] get_cheeps_of_user(user)`

Returns a list of `Cheep` instances posted by user `user`.

##### `Cheep[] get_cheeps_of_friends(user)`

Returns a list of `Cheep` instances posted by user `user`'s friends.

##### `delete_cheep(id)`

Delete's a `Cheep` with id `id`.

##### `reset()`

Resets the network to its original state: empty with no users, followers, or cheeps.


#### Example usage

```python
network = CheepNetwork()
c1 = Cheep(1, "Hello!", "will")
c2 = Cheep(2, "Hello again", "sam")
c3 = Cheep(3, "Goodbye", "will")

network.add_cheep(c1)
network.add_cheep(c2)
network.add_cheep(c3)

network.add_follower("will", "sarah")
network.add_follower("sam", "sarah")

network.get_tweets_by_id(1) # Returns the Cheep by 'will'
network.get_cheeps_of_user("will") # Returns all Cheeps by user 'will'
network.get_cheeps_of_friends("sarah") # Returns all Cheeps by 'will' and 'sam'
```

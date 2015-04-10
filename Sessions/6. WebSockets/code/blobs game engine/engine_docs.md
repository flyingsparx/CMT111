# Blobs simple game engine

This file contains the documentation for the front-end and back-end helper functions for the very simple Blobs game shown in lectures.

You will need to use a Python web application to wire-up the parts to make the game available to multiple simultaneous players using the WebSockets API.

The game allows players to move blobs around the board to eat the food. Once a player eats a piece of food, a new piece will be spawned and that player receives a point. When a certain point threshold is reached by a player then that player should be declared the winner and the game ends.

## Front end

Include the script `blobs_frontend_engine.js` in your HTML code.

This script contains the code necessary to load and run the game. It will handle all the required rendering of simple game objects and the map itself. All interaction with the game board is achieved through the `Game` object.

In your own JavaScript code, you can create and initialise a new `Game` object as follows:

```javascript
var game = new Game();
game.init();
```

This will cause the game board to be drawn. Further information on the methods exposed by `Game` is provided below.

### `Game()`
Construct a new `Game` instance.

### `Game.init()`
Draw and initialise the game board. Optionally, this method accepts an `id` attribute representing the ID of a DOM element you'd like the game to be rendered insde of. If this ID is not specified, a new element will be created for you.

### `Game.update_player(Player obj)`
Update the position of a player on the board. The player object needs to contain at least the following fields:

* `name` - the name of the player
* `x` - the numeric x-coordinate of the player
* `y` - the numeric y-coordinate of the player
* `score` - the numeric score of the player
* `colour` - the colour with which to display the player

All of this data is generated for you by the backend engine, so don't worry about generating this yourself.

### `Game.update_food(Food obj)`
Update the position of the food on the board. The food object needs to contain at least the following fields:

* `x` - the numeric x-coordinate of the food
* `y` - the numeric y-coordinate of the food

As with the players, this information is generated for you by the backend.

### Example usage

```javascript 
var game = Game();

... // receive information about players from server
for(var i = 0; i < server_data.players.length; i++){
    game.update_player(server_data.players[i]); // See below for format of returned data from server
}

... // receive information about food from server
game.update_food(server_data.food);
```

This code will automatically update the game to display the current state of the players and the food.


## Back end

The module `blobs_backend_engine.py` contains three classes to assist with running the game, however most implementations will usually only need the `Game` class:

```python
from blobs_backend_engine import Game
```

The other classes are `Player` and `Food` - both of which are created and managed by instances of `Game`.

Below is an overview of the three classes.

### `Game`

This class represents the game itself and all interaction with the game should be made through interaction with an object of this type. Method overview:

#### `Game()`
Construct a new `Game` instance. Optionally pass a `winning_score` argument to specify the score that users must reach to win the game. By default, this is `10`.

#### `Game.add_player(Player str)`
Add a new player to the game. This method must be called before the game is started.

#### `Game.start()`
Start the game. After this point, no players may be added but players can now be moved.

#### `Game.move_player(Player str, Direction str)`
Move the player with the specified name in the specified direction, where direction is in `{"up", "down", "left", "right"}`. This method can only be called if the game has been started.

The game will check whether the person has moved over the food and will ensure that the player stays within the limits of the game map.

#### Instance variables

The following attributes may help you manage the game:

* `Player[] Game.players` - list of `Player` objects currently in the game
* `Food Game.food` - the current food object to be eaten in the game
* `int Game.winning_score` - the score needed to win the game (default is `10`)
* `bool Game.is_alive` - whether the game is alive. This is `True` after the game is initialised and _before_ the game has been won
* `bool Game.is_started` - whether the game has started. This is `False` until `start()` is called


### `Food`

This class represents the food piece on the game to be eaten by players. Objects of this class are initialised and maintained by `Game`, so you don't need to worry about constructing new ones yourself. The game will automatically create new instances of `Food` each time the old one is eaten.

#### `Food()`
Construct a new piece of food with random coordinates. The `Game` class handles creation of these objects.

#### `dict Food.to_dict()`
Return a dictionary of the x/y coordinates of the object in format: `{x: <X_COORDINATE>, y: <Y_COORDINATE}`. This is useful for returning as JSON to web browsers.

#### Instance variables

* `int Food.x` - the x-coordinate of the food object
* `int Food.y` - the y-coordinate of the food object


### `Player`

This class represents a player on the board. Objects of this class are initialised and maintained by `Game`.

#### `Player(Name str, Colour str)`
Construct a new player object with random coordinates. Don't initialise this yourself. Instead, you should use the `Game.add_player()` method.

#### `dict Player.to_dict()`
Return a dictionary of the player's information in format:
```json
{
    name: NAME,
    x: X_COORDINATE,
    y: Y_COORDINATE,
    colour: COLOUR,
    score: SCORE
}
```

This is useful for returning as JSON to a web browser.

#### Instance variables

* `str Player.name` - the player's name
* `int Player.x` - the x-coordinate of the player
* `int Player.y` - the y-coordinate of the player
* `int Player.score` - the player's score
* `str Player.colour` - the colour the player is rendered as
* `bool Player.winnder` - whether the player has won yet


### General

In general, the game end can be tested for cases where `Game.is_started` is `True` and `Game.is_alive` is `False`. Under these circumstances, one of the players has won the game.

### Example usage

```python
game = Game(winning_score = 5)
game.add_player("will")
game.add_player("sarah")

... # some time later

game.move_player("will", "up")

... # some time later

# Build a dictionary of game info (food and players) to return to client:
game_info = {}
game_info['food'] = game.food.to_dict()
game_info['players'] = []
for player in game.players:
    game_info['players'].append(player.to_dict())
return json.dumps(game_info)

... # some time later

if game.is_started and not game.is_alive:
    for player in game.players:
        if player.winner = True
            print player.name+" wins the game."
```

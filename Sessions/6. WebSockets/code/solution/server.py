from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

from game_engine import Game
import random,json

app = Flask(__name__)
socketio = SocketIO(app)

num_players = 2
winning_score = 2
game = Game()
game_ended = False

@app.route('/')
def index():
    return render_template('./game.html')

def start_game():
    broadcast_game_info()

def broadcast_game_info():
    game_info = {}
    game_info['players'] = []
    for player in game.players:
        game_info['players'].append(player.to_dict())
        if player.score == winning_score:
            emit('game end', {'winner':player.name,'score':player.score}, broadcast=True)
            game_ended = True
    game_info['food'] = game.food.to_dict()
    emit('game info', game_info, broadcast=True)

@socketio.on('new player')
def add_player(player_name):
    game.add_player(player_name)
    if len(game.players) == num_players:
        start_game()

@socketio.on('update player')
def update_player(info):
    info = json.loads(info)
    game.move_player(info['name'], info['direction'])
    broadcast_game_info()
    

app.debug=True
socketio.run(app, host='0.0.0.0', port=5000)

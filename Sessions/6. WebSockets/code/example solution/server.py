from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import json

from game_engine import Game

app = Flask(__name__)
socketio = SocketIO(app)

num_players = 2
game = Game(winning_score = 10)
restart_flag = False

@app.route('/')
def index():
    return render_template('game.html', players=game.players, players_needed=num_players-len(game.players))

def broadcast_game_info():
    game_info = {}
    game_info['players'] = []
    for player in game.players:
        game_info['players'].append(player.to_dict())
        if player.winner is True:
            emit('game end', {'winner':player.name,'score':player.score}, broadcast=True)
    game_info['food'] = game.food.to_dict()
    emit('game info', game_info, broadcast=True)

@socketio.on('start game')
def start_game():
    if len(game.players) == num_players:
        game.start()
        broadcast_game_info()

@socketio.on('restart game')
def restart_game():
    global game
    game = Game()
    emit('game restarted', None, broadcast=True)

@socketio.on('player count')
def update_player_count(msg):
    if not game.is_started:
        try:
            num_players = int(msg)
            emit('new player count', {'players_needed':num_players-len(game.players), 'total_players_needed':num_players}, broadcast=True)
        except:
            pass

@socketio.on('new player')
def add_player(player_name):
    if game.is_alive and not game.is_started:
        game.add_player(player_name)
        p_list = []
        for player in game.players:
            p_list.append(player.to_dict())
        emit('player joined', {'players':p_list, 'players_needed':num_players-len(game.players)},broadcast=True)

@socketio.on('update player')
def update_player(info):
    if game.is_alive and game.is_started:
        info = json.loads(info)
        game.move_player(info['name'], info['direction'])
        broadcast_game_info()
    

app.debug=True
socketio.run(app, host='0.0.0.0', port=5000)

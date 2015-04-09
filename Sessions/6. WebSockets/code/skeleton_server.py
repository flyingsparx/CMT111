from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import json

from game_engine import Game

app = Flask(__name__)
socketio = SocketIO(app)

# This method is a standard route (e.g. GET request for returning HTML)
@app.route('/')
def index():
    return render_template('web_page_in_templates_directory.html')


# This method is a websocket route fired when data arrives as 'message'
@socketio.on('message')
def on_message(message):
    response = do_something_with_message(message)
    emit('response key', response)


# This is a standard Python function which broadcasts to all connected clients
def do_a_broadcast(message):
    emit('broadcast message', message, broadcast=True)
    

# Config and start server
app.debug=True
socketio.run(app, host='0.0.0.0', port=5000)

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import json, time

app = Flask(__name__)
socketio = SocketIO(app)

# This method is a standard route (e.g. GET request for returning HTML)
@app.route('/')
def index():
    return render_template('client.html')


# This is a standard Python function
def do_something_with_message(message):
    return "Server's response to message "+str(message['message_count'])+" that had text "+message['message']


# This method is a websocket route fired when data arrives as 'message'
@socketio.on('message')
def on_message(message):
    response = do_something_with_message(message)
    emit('response key', response)


# This method is a websocket route fired when data arrives as 'broadcast message'
@socketio.on('broadcast message')
def on_broadcast(message):
    emit('broadcast message', {'message':message, 'time':int(time.time())}, broadcast=True)


# Config and start server
app.debug=True
socketio.run(app, host='0.0.0.0', port=5000)

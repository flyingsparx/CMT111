# Web server exposing a RESTful API for a Twitter clone: Cheep
#
# Example requests:
# GET /users (return list of users)
# POST /users ?name=will (create a new user)
# POST /users/will/cheeps ?text=Hello! (create a new cheep with text 'Hello!')
# DELETE /users/will/cheeps/1 (delete will's cheep with id 1)
# PUT /users/will/cheeps/1 ?text=Hello! (update cheep with new text)
# GET /users/will/home_timeline (get all cheeps of will's friends)
# POST /users/will/followers ?follower=sam (adds user sam as a follower of will)
# GET /users/will/friends (get all users that will follows)



from flask import Flask, make_response, request
import json, random
from cheep_utils import Cheep, SentimentAnalyser, CheepEngine

app = Flask(__name__)



# Initialise our network

cheep_eng = CheepEngine()
senti_analyser = SentimentAnalyser("KEY")


# Couple o' helper methods

def build_response():
    response = make_response()
    response.status_code = 200
    response.mimetype = "application/json"
    response.headers.add("Application", "Will's awesome Twitter clone")
    return response

def cheep_dict(cheep):
    return {'id':cheep.id,'user':cheep.user,'text':cheep.text,'sentiment':cheep.sentiment}

def jsonify(data):
    return json.dumps(data, indent=4)


# Routing methods


@app.route("/users", methods=["GET", "POST", "DELETE"])
def user_endpoint():
    response = build_response()
    if request.method == "GET":
        response.data = jsonify(cheep_eng.get_users())
    elif request.method == "POST":
        try:
            cheep_eng.create_user(request.form['name'])
            response.status_code = 201
        except:
            response.status_code = 409
    elif request.method == "DELETE":
        if cheep_eng.get_user(request.form['name']) is not None:
            cheep_eng.delete_user(request.form['name'])
        else:
            response.status_code = 404
    return response


@app.route("/users/<name>/followers", methods=["GET", "POST", "DELETE"])
def followers(name):
    response = build_response()
    if cheep_eng.get_user(name) is None:
        response.status_code = 404
    elif request.method == "GET":
        response.data = jsonify(cheep_eng.get_followers(name))
    elif request.method == "POST":
        if cheep_eng.get_user(request.form['follower']) is not None:
            cheep_eng.add_follower(name, request.form['follower'])
            response.status_code = 201
        else:
            response.status_code = 404
    elif request.method == "DELETE":
        if cheep_eng.get_user(request.form['follower']) is not None:
            cheep_eng.delete_follower(name, request.form['follower'])
        else:
            response.status_code = 404

    return response

@app.route("/users/<name>/friends", methods=["GET"])
def friends(name):
    response = build_response()
    if(cheep_eng.get_user(name)) is None:
        response.status_code = 404
    else:
        response.data = cheep_eng.get_friends(name)
    return response


@app.route("/users/<name>/cheeps", methods=["GET", "POST"])
def user_cheeps(name):
    response = build_response()
    if cheep_eng.get_user(name) is None:
        response.status_code = 404
    elif request.method == "GET":
        cheeps = []
        for cheep in cheep_eng.get_cheeps_of_user(name):
            cheeps.append(cheep_dict(cheep))
        response.data = jsonify(cheeps)
    elif request.method == "POST":
        try:
            cheep = Cheep(random.randint(0, 10000), request.form['text'], name)
            cheep.sentiment = senti_analyser.get_cheep_sentiment(cheep)
            cheep_eng.add_cheep(cheep)
            response.status_code = 201
            response.data = jsonify(cheep_dict(cheep))
        except:
            response.status_code = 409
    return response

@app.route("/users/<name>/cheeps/<id>", methods=["DELETE", "PUT"])
def cheep_id(name, id):
    response = build_response()
    if cheep_eng.get_user(name) is None or cheep_eng.get_cheep_by_id(id) is None:
        response.status_code = 404
    elif request.method == "DELETE":
        cheep_eng.delete_cheep(id)
    elif request.method == "PUT":
        cheep = cheep_eng.get_cheep_by_id(id)
        cheep.text = request.form['text']
        cheep_eng.delete_cheep(id)
        cheep_eng.add_cheep(cheep)
        response.data = jsonify(cheep_dict(cheep))
    return response

@app.route("/cheeps", methods=["GET"])
def cheeps():
    response = build_response()
    cheeps = []
    for cheep in cheep_eng.get_cheeps():
        cheeps.append(cheep_dict(cheep))
    response.data = jsonify(cheeps)
    return response

@app.route("/cheeps/<id>", methods=["GET"])
def cheeps_id(id):
    response = build_response()
    cheep = cheep_eng.get_cheep_by_id(id)
    if cheep is None:
        response.status_code = 404
    else:
        response.data = jsonify(cheep_dict(cheep))
    return response

@app.route("/cheeps/sentiment/<sentiment>", methods=["GET"])
def cheep_sentiment(sentiment):
    response = build_response()
    cheeps = []
    for cheep in cheep_eng.get_cheeps_by_sentiment(sentiment):
        cheeps.append(cheep_dict(cheep))
    response.data = jsonify(cheeps)
    return response

@app.route("/users/<name>/home_timeline", methods=["GET"])
def home_timeline(name):
    response = build_response()
    if cheep_eng.get_user(name) is None:
        response.status_code = 404
    else:
        cheeps = []
        for cheep in cheep_eng.get_cheeps_of_friends(name):
            cheeps.append(cheep_dict(cheep))
        response.data = jsonify(cheeps)
    return response
    
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=80)
    

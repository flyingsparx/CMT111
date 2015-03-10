# Simple Flask webserver demonstrating a simple web API that 
# supports HTTP methods for accessing and modifying 
# resources.
#
# Script needs to run as root (not usually recommended) as
# it's easier if I just run on port 80!



from flask import Flask, make_response, request
import json
app = Flask(__name__)



class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hobbies = []
    def get(self):
        d = {}
        d['name'] = self.name
        d['age'] = self.age
        d['hobbies'] = self.hobbies
        return d
u1 = User("Will", 26)
u2 = User("Sarah", 24)
users = []
users.append(u1.get())
users.append(u2.get())

def get_user_by_name(name):
    for user in users:
        if user['name'] == name:
            return user
    return None



# Do some web stuff:


@app.route("/users", methods=["GET","POST"])
def user_endpoint():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    if request.method == "GET":
        response.data = json.dumps(users, indent=4)
        response.mimetype = "application/json"

    elif request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        user = User(name, int(age))
        users.append(user.get())
        response.status_code = 201

    else:
        response.status_code = 405

    return response




@app.route("/users/<name>", methods=["GET","DELETE"])
def specific_user_endpoint(name):
    response = make_response()
    if request.method == "GET":
        if get_user_by_name(name) != None:
            response.data = json.dumps(get_user_by_name(name), indent=4)
            response.mimetype = "application/json"
        else:
            response.status_code = 404
    
    elif request.method == "DELETE":
        if request.headers.get('key') =='williscool':
            users.remove(get_user_by_name(name))
            response.status_code = 204
        else:
            response.status_code = 403

    else:
        response.status_code = 405

    return response



    
@app.route("/users/<name>/hobbies", methods=["GET","POST","DELETE"])
def hobbies_user_endpoint(name):
    response = make_response()
    if request.method == "GET":
        if get_user_by_name(name) != None:
            response.data = json.dumps(get_user_by_name(name)['hobbies'], indent=4)
            response.mimetype = "application/json"
        else:
            response.status_code = 404
    
    elif request.method == "POST":
        if get_user_by_name(name) != None:
            get_user_by_name(name)['hobbies'].append(request.form['hobby'])
            response.status_code = 204
        else:
            response.status_code = 404

    elif request.method == "DELETE":
        get_user_by_name(name)['hobbies'].remove(request.form['hobby'])
        response.status_code = 204

    else:
        response.status_code = 405

    return response 
    



if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=80)
    

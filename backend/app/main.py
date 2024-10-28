
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import os

basedir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(basedir, '../../frontend/templates')
static_dir = os.path.join(basedir, '../../frontend/static')

app=Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
app.config["SECRET_KEY"] =  "testing"
socketio = SocketIO(app)

rooms = {} #keep track of used room nums

def generate_unique_code(length): #generates unique room code that is not being used
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break

    return code

@app.route("/", methods=["POST", "GET"])

def home():

    session.clear() #
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code = code, name = name)
        if join != False and not code:
            return render_template("home.html", error = "Please enter a code.", code = code, name = name)
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error = "Room does not exist.", code = code, name = name)

        session["room"] = room # stores user information during a session
        session["name"] = name
        return redirect(url_for("room")) #takes user to chat room

    return render_template("home.html")

@app.route("/room", methods=["POST", "GET"])
#left off at 40:43 in the TechWithTim video
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:# only take user to a chat room if all data is input correctly, like name and room code
        return redirect(url_for("home"))

    return render_template("room.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)


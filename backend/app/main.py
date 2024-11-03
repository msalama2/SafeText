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

# Home route to display the main page
@app.route("/", methods=["GET"])
def home():
    session.clear()  # Clear the session to reset any room data
    return render_template("home.html")


# Route for joining an existing room
@app.route("/joinroom", methods=["POST", "GET"])
def join_room_page():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")

        # Validate name and room code
        if not name:
            return render_template("joinroom.html", error="Please enter a name.")
        if not code:
            return render_template("joinroom.html", error="Please enter a room code.")
        
        # Check if room exists
        if code not in rooms:
            return render_template("joinroom.html", error="Room does not exist.")

        # Store room and name in the session
        session["room"] = code
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("joinroom.html")

# Route for creating a new room
@app.route("/createroom", methods=["POST", "GET"])
def create_room_page():
    if request.method == "POST":
        name = request.form.get("name")

        # Validate name
        if not name:
            return render_template("createroom.html", error="Please enter a name.")

        # Generate a unique room code and initialize the room
        room = generate_unique_code(4)
        rooms[room] = {"members": 0, "messages": []}

        # Store room and name in the session
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("createroom.html")

# Route for displaying the chat room page
@app.route("/room", methods=["GET"])
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", room=room)

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=8000)
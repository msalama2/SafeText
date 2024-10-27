
from flask import Flask, render_template, request, session, redirect
#from flask_socketio import SocketIO
#from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import os

basedir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(basedir, '../../frontend/templates')
static_dir = os.path.join(basedir, '../../frontend/static')

app=Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
app.config["SECRET_KEY"] =  "testing"
#socketio = SocketIO(app)

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)


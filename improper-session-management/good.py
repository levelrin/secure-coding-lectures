from flask import session, Flask, render_template, request, redirect, url_for
from random import randbytes

app = Flask(__name__)

# A secret key to generate a session ID
app.secret_key = randbytes(32)

# User credentials.
users = {
    "test01": {
        "displayName": "test01",
        "password": "1111",
        "items": ["Apple", "Banana", "Orange"]
    },
    "test02": {
        "displayName": "test02",
        "password": "2222",
        "items": ["Kiwi", "Peach", "Pineapple"]
    },
    "test03": {
        "displayName": "test03",
        "password": "3333",
        "items": ["Plum", "Strawberry", "Mango"]
    }
}

# A dictionary to store active sessions.
# Key - session id
# Value - user object
sessions = {}


@app.route("/")
def index():
    session_id = None
    if "username" in session:
        session_id = session["username"]
    global sessions
    return render_template("index.html", session_id=session_id, sessions=sessions)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # Load the login page.
        return render_template("login.html")
    elif request.method == "POST":
        # Process the login action.
        username = request.form["username"]
        password = request.form["password"]
        global users
        if username in users and users[username]["password"] == password:
            session["username"] = username
            session_id = session["username"]
            sessions[session_id] = users[username]
            return redirect(url_for("index"))
        else:
            return "login failed"
    else:
        return "Method Not Allowed", 405

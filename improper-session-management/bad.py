import functools

from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

# We will assign session id incrementally.
current_session_id = 0

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


# This is a decorator for route function.
# It will check the URL to see if there is the 'session_id' URL parameter.
# If the 'session_id' doesn't exist, it will add the 'session_id' URL parameter
# and redirect the page into the redirect_endpoint.
def with_session(redirect_endpoint):
    def new_route(original_route):
        @functools.wraps(original_route)
        def new_behavior(*args, **kwargs):
            if request.method == "GET":
                session_id = request.args.get("session_id")
            else:
                # We assume it's a POST request.
                session_id = request.form.get("session_id")
            if session_id is None:
                global current_session_id
                session_id = current_session_id
                current_session_id = current_session_id + 1
                return redirect(url_for(redirect_endpoint, session_id=session_id))
            else:
                return original_route(*args, **kwargs)
        return new_behavior
    return new_route


@app.route("/")
@with_session("index")
def index():
    session_id = request.args.get("session_id")
    global sessions
    return render_template("index.html", session_id=session_id, sessions=sessions)


@app.route("/login", methods=["GET", "POST"])
@with_session("login")
def login():
    if request.method == "GET":
        # Load the login page.
        session_id = request.args.get("session_id")
        return render_template("login.html", session_id=session_id)
    elif request.method == "POST":
        # Process the login action.
        username = request.form["username"]
        password = request.form["password"]
        global users
        if username in users and users[username]["password"] == password:
            session_id = request.form.get("session_id")
            sessions[session_id] = users[username]
            return redirect(url_for("index", session_id=session_id))
        else:
            return "login failed"
    else:
        return "Method Not Allowed", 405


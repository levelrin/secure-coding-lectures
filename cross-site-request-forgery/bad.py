from random import randbytes
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)


# A secret key to generate a session ID
app.secret_key = randbytes(32)

# User credentials.
users = {
    "test01": {
        "displayName": "test01",
        "password": "1111",
        "items": []
    },
    "test02": {
        "displayName": "test02",
        "password": "2222",
        "items": []
    },
    "test03": {
        "displayName": "test03",
        "password": "3333",
        "items": []
    }
}


@app.route("/")
def index():
    user = None
    if "username" in session:
        user = session["username"]
    return render_template("index-bad.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username]["password"] == password:
        session["username"] = users[username]
        return redirect(url_for("index"))
    else:
        return "Login failed"


@app.route("/logout", methods=["POST"])
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("index"))


@app.route("/addItem", methods=["POST"])
def add_item():
    if "username" in session:
        user = session["username"]
        item = request.form["item"]
        user["items"].append(item)
        session["username"] = user
        return redirect(url_for("index"))
    else:
        return "You are not logged in"


# We are using HTML form to call this endpoint.
# Unfortunately, HTML form does not support DELETE method.
# As a workaround, we are using POST method.
@app.route("/removeItem", methods=["POST"])
def remove_item():
    if "username" in session:
        user = session["username"]
        item = request.form["item"]
        user["items"].remove(item)
        session["username"] = user
        return redirect(url_for("index"))
    else:
        return "You are not logged in"

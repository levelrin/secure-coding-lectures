from flask import Flask, url_for, redirect, request, render_template, session
import subprocess

app = Flask(__name__)
# we must set the secret key to use session.
app.secret_key = "Yoi Yoi"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read", methods=["POST"])
def read():
    # Obtain the file name
    file_name = request.form["file_name"]

    # This method neutralize the externally-provided value.
    result = subprocess.run(
        ['cat', f'/usr/local/os-command-injection/{file_name}'],
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8')
    session["content"] = result

    # Redirect the user into the home page
    return redirect(url_for("content"))


@app.route("/content")
def content():
    return session.get("content")

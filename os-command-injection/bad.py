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

    cmd = f'cat /usr/local/os-command-injection/{file_name}'
    # This is vulnerable to OS command injection.
    # For example, if the value of file_name is "Hey.txt && cat /usr/admin/secret",
    # the entire OS command would be "cat /usr/local/os-command-injection/Hey.txt && cat /usr/admin/secret"
    # It will disclose the secret file to the hacker.
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    session["content"] = result

    # Redirect the user into the home page
    return redirect(url_for("content"))


@app.route("/content")
def content():
    return session.get("content")

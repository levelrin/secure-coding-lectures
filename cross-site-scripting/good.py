from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/echo", methods=["POST"])
def echo():
    # render_template() is more secure than render_template_string().
    # It sanitizes the user input, which is the content variable in this case.
    return render_template("echo.html", content=request.form["content"])

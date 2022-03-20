from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/echo", methods=["POST"])
def echo():
    # render_template_string() does not sanitize the user input.
    # It's possible to inject javascript code into the template.
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Cross-Site Scripting</title>
        </head>
        <body>
            <h3>You said:</h3>
            <p>
               %s
            </p>
        </body>
        </html>
        """ % request.form["content"]
    )

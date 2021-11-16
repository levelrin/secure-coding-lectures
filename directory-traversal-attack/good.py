import os

from flask import Flask, request, send_file, render_template, Response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/open_file', methods=["GET"])
def open_file():
    # This will extract the file name if the user input the path.
    file_name = os.path.basename(
        request.args.get('file_name')
    )
    print(f"File name: ${file_name}")

    file_path = os.path.join(
        '/usr/local/directory-traversal-attack',
        file_name
    )
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return render_template('404.html'), 404

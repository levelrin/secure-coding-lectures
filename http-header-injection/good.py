import flask
from flask import Flask

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print("path: ", path)
    response = flask.Response("Yoi Yoi")
    response.headers["Location"] = "http://localhost:7777/" + path
    response.status_code = 302
    return response

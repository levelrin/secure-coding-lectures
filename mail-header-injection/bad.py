import subprocess
from urllib.parse import unquote
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/survey", methods=["GET"])
def echo():
    mail_address = unquote(request.args.get("mail-address"))
    print("mail-address: " + mail_address)

    # We need to create a file that contains the mail header and body.
    # We will send a mail with the content of this file.
    temp_file = open("/tmp/raw", "w+")
    temp_file.write(f"""From: Survey <survey@localhost>
To: {mail_address}
Subject: Thank you for completing our survey!

Here is the coupon code: 1234567890
""")
    temp_file.close()

    # Send a mail via mutt command.
    subprocess.run(
        ["mutt", "-H", "/tmp/raw"],
        input="",
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8')

    return "Thank you for completing the survey! Please check your email for confirmation."

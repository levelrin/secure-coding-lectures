import smtplib
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

    # Using SMTP library will prevent the mail header injection.
    with smtplib.SMTP("localhost", 25) as smtp:
        smtp.sendmail(
            "survey@localhost",
            mail_address,
            """Subject: Thank you for completing our survey!

Here is the coupon code: 1234567890
"""
        )
    return "Thank you for completing the survey! Please check your email for confirmation."

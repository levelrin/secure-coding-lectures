from flask import Flask, url_for, redirect, request, render_template
import psycopg2

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    # Obtain the user id and name
    user_id = request.form["user_id"]
    user_name = request.form["user_name"]
    print(f"id: {user_id}, name: {user_name}")

    # Connect to the database
    connection = psycopg2.connect(
        host="sql-injection-sql-injection-db-1",
        database="sql-injection",
        user="postgres",
        password="postgres"
    )

    # Cursor is for executing the SQL commands
    cursor = connection.cursor()

    # Insert a new user into the database.
    # This code is secure from the SQL injection attack.
    # It will replace the placeholder values as literal strings :D
    cursor.execute(
        "INSERT INTO users (id, name) VALUES (%s, %s);",
        (user_id, user_name)
    )

    # The SQL command won't be executed without this method call
    connection.commit()

    # Close the resources after we are done with the database manipulation
    cursor.close()
    connection.close()

    # Redirect the user into the home page
    return redirect(url_for("index"))

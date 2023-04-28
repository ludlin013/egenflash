from flask import *
from cryptography.fernet import Fernet
import os
from waitress import serve

key = Fernet.generate_key()
fernet = Fernet(key)


app = Flask(__name__)


@app.route("/")
def index():
    temp = os.listdir(os.path.join("static", "templates"))

    templates = {}

    for x in temp:
        with open(os.path.join("static", "templates", x), encoding="utf-8") as f:
            content = f.read()
        templates[x] = content.replace("\n", "\\n")

    # print(templates)

    return render_template("index.html", templates=templates)


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    message = request.form["message"]

    encrypt = fernet.encrypt(message.encode())

    with open(os.path.join("static", "messages", encrypt.decode()), "w") as f:
        f.write("")

    link = "pw.ecitpro.se/message?file=" + encrypt.decode()

    return render_template("encrypt.html", link=link)


@app.route("/message")
def message():
    message = "/view?file=" + request.args.get("file")

    return render_template("message.html", message=message)


@app.route("/view")
def view():
    file = request.args.get("file")

    message = None

    if os.path.isfile(os.path.join("static", "messages", file)):
        os.remove(os.path.join("static", "messages", file))
        message = fernet.decrypt(file.encode()).decode()

    return render_template("view.html", message=message)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port="8080")
    serve(app, host="0.0.0.0", port=8080)

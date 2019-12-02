from flask import *
from threading import Thread
app = Flask(__name__)
app.config['SECRET_KEY'] = "SomeSecretText"
@app.route("/")
def home():
    return "Alive"


def run():
    app.run(host="127.0.0.1", port=12709)


def keep_alive():
    server = Thread(target=run)
    server.start()
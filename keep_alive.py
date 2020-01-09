from flask import *
from threading import Thread
app = Flask(__name__)
app.config['SECRET_KEY'] = "SomeSecretText"
@app.route("/")
def home():
    return "Alive"


@app.route("/ping")
def ping():
    return "Pong!! Rebooting bot if it isn't on"


@app.route("/kill")
def kill():
    exit()


def run():
    app.run(host="127.0.0.1", port=80)


def keep_alive():
    server = Thread(target=run)
    server.start()

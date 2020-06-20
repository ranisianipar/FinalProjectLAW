from flask import request, jsonify
from services.timer import TimerService

import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "Hello World! Server 5 here."

timer = TimerService()

timer.run_timer_async()

app.run(port=5005)
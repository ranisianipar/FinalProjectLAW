from flask import request, jsonify, render_template
from services.downloader import DownloadService
from services.consumer import ConsumerService
from services.publisher import PublisherService
from services.uploader import UploaderService
from config import EXCHANGE_DIRECT, TOPIC_FILE_UPLOAD

import flask
import json
import requests
import threading

EXCHANGE_NAME_CONSUME = EXCHANGE_DIRECT
EXCHANGE_TYPE_CONSUME = 'direct'


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "Hello World! Server 2 here."

consumer = ConsumerService(exchange_name=EXCHANGE_NAME_CONSUME, exchange_type=EXCHANGE_TYPE_CONSUME, topics=[TOPIC_FILE_UPLOAD])
downloader = DownloadService()
uploader = UploaderService()

def callback_download(ch, method, properties, body):
    payload = json.loads(body)
    rk = method.routing_key
    print(f'[SERVER_2] Message Received! Routing Key: {rk}; Payload: {payload}')
    
    # {<file_id>:<file_name>}
    files_dict = downloader.bulk_download(payload)
    uploader.bulk_upload(files_dict)


consumer.bind_queue_callback(TOPIC_FILE_UPLOAD, callback_download)

thread = threading.Thread(target=consumer.start, args=())
thread.start()

app.run(port=5002)
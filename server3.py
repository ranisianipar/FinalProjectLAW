from config import EXCHANGE_TOPIC, TOPIC_CHUNK_UPLOAD
from flask import request, jsonify
from services.compressor import ZipService
from services.consumer import ConsumerService

import flask
import json
import threading

EXCHANGE_NAME_CONSUME = EXCHANGE_TOPIC
EXCHANGE_TYPE_CONSUME = 'topic'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "Hello World! Server 3 here."

@app.route('/zip', methods=['GET'])
def ziptest():
    zipper = ZipService()
    zipper.zip()
    return "Zip done."

consumer = ConsumerService(exchange_name=EXCHANGE_NAME_CONSUME, exchange_type=EXCHANGE_TYPE_CONSUME, topics=[TOPIC_CHUNK_UPLOAD])
zipper = ZipService()

def callback_compress(ch, method, properties, body):
    payload = json.loads(body)
    rk = method.routing_key

    file_id = payload['file_id']
    file_name = payload['file_name']
    data = payload['data']
    total_file = payload['total_file']
    total_length = payload['total_length']

    zipper.start_stream(file_id=file_id, file_name=file_name, chunk=data, total_file=total_file,total_length=total_length)
    print(f'[SERVER_3] Message Received! Routing Key: {rk}; File: {file_name}; Total Length: {total_length}')
    


consumer.bind_queue_callback(TOPIC_CHUNK_UPLOAD, callback_compress)

# thread = threading.Thread(target=, args=())
# thread.start()

consumer.start()

app.run(port=5003)
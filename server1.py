from flask import request, jsonify, render_template
from services.publisher import PublisherService
from services.consumer import ConsumerService
from config import (
    EXCHANGE_DIRECT,
    EXCHANGE_TOPIC,
    PORT, # app
    RABBITMQ_HOST, 
    RABBITMQ_USER, 
    RABBITMQ_PASS, 
    RABBITMQ_PORT,
    RABBITMQ_WEBSOCKET_URL,
    RABBITMQ_VHOST, 
    TOPIC_COMPRESS,
    TOPIC_DOWNLOAD,
    TOPIC_FILE_UPLOAD,
    TOPIC_TIMER
)

import flask
import requests


EXCHANGE_NAME_PUBLISH = EXCHANGE_DIRECT
EXCHANGE_TYPE_PUBLISH = 'direct'
EXCHANGE_NAME_CONSUME = EXCHANGE_TOPIC
EXCHANGE_TYPE_CONSUME = 'topic'

app = flask.Flask(__name__, template_folder='template', static_folder='static')
app.config["DEBUG"] = True

def get_subs_topic(routing_key):
    return f'/exchange/{EXCHANGE_NAME_CONSUME}/{routing_key}'

def get_file_id(id):
    return f'file_{id}'

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html',
                            file_id_1=get_file_id(1),
                            file_id_2=get_file_id(2),
                            file_id_3=get_file_id(3),
                            file_id_4=get_file_id(4),
                            file_id_5=get_file_id(5),
                            file_id_6=get_file_id(6),
                            file_id_7=get_file_id(7),
                            file_id_8=get_file_id(8),
                            file_id_9=get_file_id(9),
                            file_id_10=get_file_id(10)
                            )

@app.route('/download', methods=['POST'])
def download():
    publisher = PublisherService(exchange_name=EXCHANGE_NAME_PUBLISH, exchange_type=EXCHANGE_TYPE_PUBLISH)
    
    # get all urls
    topic_url_dict = {}
    for i in range(1,11):
        topic = get_file_id(i)
        url = request.form[topic]
        if url != '':
            topic_url_dict[topic] = url
    publisher.send_msg_to_rk(msg=topic_url_dict, rk=TOPIC_FILE_UPLOAD)

    return render_template('download.html',
                            rabbitmq_host=RABBITMQ_VHOST,
                            rabbitmq_user=RABBITMQ_USER,
                            rabbitmq_password=RABBITMQ_PASS,
                            topic_compress=get_subs_topic(TOPIC_COMPRESS),
                            topic_timer=get_subs_topic(TOPIC_TIMER),
                            topic_download=get_subs_topic(TOPIC_DOWNLOAD),
                            file_id_1=get_file_id(1),
                            file_id_2=get_file_id(2),
                            file_id_3=get_file_id(3),
                            file_id_4=get_file_id(4),
                            file_id_5=get_file_id(5),
                            file_id_6=get_file_id(6),
                            file_id_7=get_file_id(7),
                            file_id_8=get_file_id(8),
                            file_id_9=get_file_id(9),
                            file_id_10=get_file_id(10),
                            url_1=topic_url_dict.get(get_file_id(1), ''),
                            url_2=topic_url_dict.get(get_file_id(2), ''),
                            url_3=topic_url_dict.get(get_file_id(3), ''),
                            url_4=topic_url_dict.get(get_file_id(4), ''),
                            url_5=topic_url_dict.get(get_file_id(5), ''),
                            url_6=topic_url_dict.get(get_file_id(6), ''),
                            url_7=topic_url_dict.get(get_file_id(7), ''),
                            url_8=topic_url_dict.get(get_file_id(8), ''),
                            url_9=topic_url_dict.get(get_file_id(9), ''),
                            url_10=topic_url_dict.get(get_file_id(10), ''),
                            websocket_url=RABBITMQ_WEBSOCKET_URL
                        )
app.run(port=PORT)
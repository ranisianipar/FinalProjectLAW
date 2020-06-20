import os
import yaml

with open('./config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = config['port']

ENV = 'development'
# ENV = 'production'

EXCHANGE_DIRECT = '1606885025_DIRECT'
EXCHANGE_TOPIC = '1606885025_TOPIC'

RABBITMQ_HOST = config['rabbitmq'][ENV]['host']
RABBITMQ_USER = config['rabbitmq'][ENV]['user']
RABBITMQ_PASS = config['rabbitmq'][ENV]['pass']
RABBITMQ_VHOST = config['rabbitmq'][ENV]['vhost']
RABBITMQ_WEBSOCKET_PORT = config['rabbitmq']['websocket']['port']
RABBITMQ_WEBSOCKET_URL = f'http://localhost:{RABBITMQ_WEBSOCKET_PORT}/stomp'
RABBITMQ_PORT = config['rabbitmq']['port']

TOPIC_COMPRESS = config['topic']['compress']
TOPIC_DOWNLOAD = config['topic']['download']
TOPIC_TIMER = config['topic']['timer']
TOPIC_FILE_UPLOAD = config['topic']['file_upload']
TOPIC_CHUNK_UPLOAD = config['topic']['chunk_upload']

# URL_SERVER_2 = config['url']['server_2']
# URL_SERVER_3 = config['url']['server_3']
# URL_SERVER_4 = config['url']['server_4']
# URL_SERVER_5 = config['url']['server_5']

WEBSOCKET_PORT = config['rabbitmq']['port']
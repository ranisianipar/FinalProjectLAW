import pika
import json
from config import (
    RABBITMQ_HOST, 
    RABBITMQ_USER, 
    RABBITMQ_PASS, 
)
class PublisherService:
    def __init__(self, exchange_name, exchange_type):
        credentials = pika.PlainCredentials(username=RABBITMQ_USER,password=RABBITMQ_PASS)
        self.parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        self.connection = pika.BlockingConnection(self.parameters)

        self.exchange_name = exchange_name
        self.exchange_type = exchange_type

        self.channel = self.connection.channel()

        self.setup_exchange()

    def create_channel(self):
        self.channel = self.connection.channel()
        self.setup_exchange()
        return self.channel

    def setup_exchange(self):
        print(f'Publisher declare exchange, name: {self.exchange_name}, type: {self.exchange_type}')
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)

    def send_msg_to_rk(self, msg, rk):
        print(f' [x] Message sent. Routing Key: {rk}; Exchange Name: {self.exchange_name}')
        self.channel.basic_publish(
            exchange=self.exchange_name, 
            routing_key=rk, 
            body=json.dumps(msg),
            properties=pika.BasicProperties(content_type='application/json', delivery_mode=1)
        )

    def close_channel(self, ch):
        ch.close()

    def close_connection(self):
        self.connection.close()
    def start(self):
        print('dummy')
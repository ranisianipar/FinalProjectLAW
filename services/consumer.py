import pika
from config import (
    RABBITMQ_HOST, 
    RABBITMQ_USER, 
    RABBITMQ_PASS, 
)

class ConsumerService:
    def __init__(self, exchange_name, exchange_type, topics):
        credentials = pika.PlainCredentials(username=RABBITMQ_USER,password=RABBITMQ_PASS)
        self.parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        self.connection = pika.BlockingConnection(self.parameters)

        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        
        self.channel = self.connection.channel()

        self.setup_exchange(exchange_name, exchange_type)        

        self.topics = topics
        self.prepare_queue(topics)
        self.bind_queue_rk(topics)

    def setup_exchange(self, exchange_name, exchange_type):
        self.exchange_name = exchange_name

        print(f'Consumer declare exchange, name: {exchange_name}, type: {exchange_type}')
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=exchange_type)

    def prepare_queue(self, queue_names):
        for q in queue_names:
            self.channel.queue_declare(queue=q)

    # Routing Key == Queue Name
    def bind_queue_rk(self, topics):
        for t in topics:
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=t,
                routing_key=t
            )

    def bind_queue_callback(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def start(self):
        self.channel.start_consuming()

    def close_channel(self):
        self.channel.close()
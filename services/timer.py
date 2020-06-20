from datetime import datetime
from services.publisher import PublisherService
from config import EXCHANGE_TOPIC, TOPIC_TIMER
import pika
import time
import threading


EXCHANGE_NAME_PUBLISH = EXCHANGE_TOPIC
EXCHANGE_TYPE_PUBLISH = 'topic'

class TimerService:
    def __init__(self):
        self.publisher = self.publisher = PublisherService(exchange_name=EXCHANGE_NAME_PUBLISH, exchange_type=EXCHANGE_TYPE_PUBLISH)

    def send_time(self, time):
        payload = {
            'time':time
        }
        self.publisher.send_msg_to_rk(msg=payload, rk=TOPIC_TIMER)
            
    def run_timer(self):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.send_time(current_time)
            print(" [x] Sent Current Time:", current_time)
            time.sleep(1)

    def run_timer_async(self):
        thread = threading.Thread(target=self.run_timer, args=())
        thread.start()

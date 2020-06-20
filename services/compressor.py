from .publisher import PublisherService
from .encryption import decode_b64str_bytes, get_secured_link
from config import EXCHANGE_TOPIC, PROJECT_DIR, TOPIC_COMPRESS
from io import BytesIO ## for Python 3

import base64
import pika
import os
import uuid
import zipfile

EXCHANGE_NAME_PUBLISH = EXCHANGE_TOPIC
EXCHANGE_TYPE_PUBLISH = 'topic'

class ZipService:
    def __init__(self):
        self.init_arc()
        self.compress_type = zipfile.ZIP_DEFLATED
        self.compressed_file = 0
        self.data_buffer = BytesIO()
        self.publisher = PublisherService(exchange_name=EXCHANGE_NAME_PUBLISH, exchange_type=EXCHANGE_TYPE_PUBLISH)

    def init_arc(self):
        uuid_str = str(uuid.uuid4())
        self.arc_name = f'{uuid_str}.zip'
        self.archive = zipfile.ZipFile(f'{PROJECT_DIR}/temp/compressed/{self.arc_name}', 'w')
        self.is_arc_closed = False

    def compress(self, file_name, data):
        if self.is_arc_closed:
            self.init_arc()
        print(f'ARC STATUS: {self.is_arc_closed}')
        self.archive.writestr(file_name, data, compress_type=self.compress_type)
        self.compressed_file += 1
        print(f'Total compressed: {self.compressed_file} files')

    def start_stream(self, file_id, file_name, chunk, total_file, total_length):
        self.write_stream(data=chunk)
        
        percentage = int( (self.data_buffer.tell()/total_length) * 100)
        self.send_progress(file_id=file_id, progress=percentage)

        if percentage == 100:
            print(f'Total File: {total_file}')
            self.flush(file_name)

        if self.compressed_file == total_file:
            link = get_secured_link(self.arc_name)
            self.close_stream(link=link)

    def write_stream(self, data):
        data_decoded = decode_b64str_bytes(data)
        self.data_buffer.write(data_decoded)
        print(f'Write data! Buffer Size: {self.data_buffer.tell()}')

    def flush(self, file_name):
        print(f'Flush In-Memory data for file: {file_name}')
        self.compress(file_name, self.data_buffer.getvalue())
        self.data_buffer = BytesIO()

    def close_stream(self, link):
        print('Compress files done! Close compressor stream.')
        self.archive.close()
        self.is_closed = True
        payload = {
            'link':link
        }
        self.publisher.send_msg_to_rk(rk=TOPIC_COMPRESS, msg=payload)
        print(f' Sent link! Link: {link}')

    def send_progress(self, file_id, progress):
        payload = {
            'file_id':file_id,
            'progress':f'{progress}%'
        }
        
        self.publisher.send_msg_to_rk(rk=TOPIC_COMPRESS, msg=payload)
        print(f' Sent progress! Compress: {file_id}; progress: {progress}%')
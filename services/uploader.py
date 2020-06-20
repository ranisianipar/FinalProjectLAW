from config import EXCHANGE_TOPIC, TOPIC_CHUNK_UPLOAD
from .publisher import PublisherService
from .encryption import encode_bytes_str

import base64
import os
import pika
import requests

PATH_DOWNLOADED_FILE = './temp/downloader'

EXCHANGE_NAME_PUBLISH = EXCHANGE_TOPIC
EXCHANGE_TYPE_PUBLISH = 'topic'

class UploaderService:
    def __init__(self):
        self.publisher = PublisherService(exchange_name=EXCHANGE_NAME_PUBLISH, exchange_type=EXCHANGE_TYPE_PUBLISH)
        self.total_file = 0

    def send_chunk(self, file_id, file_name, data_bytes, total_length):
        # Bytes converted to string using Base64 encoding
        data = encode_bytes_str(data_bytes=data_bytes)
        
        payload = {
            'file_id':file_id,
            'file_name':file_name,
            'data':data,
            'total_file':self.total_file,
            'total_length':total_length
        }
        
        self.publisher.send_msg_to_rk(msg=payload, rk=TOPIC_CHUNK_UPLOAD)
        print(f' Sent progress! Upload: {file_name}; total size: {total_length}; data-length: {len(data_bytes)}')

    def upload(self, file_id, file_name):
        file_path = f'{PATH_DOWNLOADED_FILE}/{file_name}'
        file_info = os.stat(file_path)
        total_length = int(file_info.st_size)

        chunk_size = 4096
        
        with open(file_path, "rb") as f:
            print(f'Start uploading {file_name}...')
            chunk = f.read(chunk_size)
            while chunk:
                self.send_chunk(file_id= file_id,file_name=file_name, data_bytes=chunk, total_length=total_length)
                chunk = f.read(chunk_size)
                    
    # {<file_id>:<file_name>}
    def bulk_upload(self, files_dict):
        self.total_file = len(files_dict)
        for fid in files_dict:
            self.upload(fid, files_dict[fid])
        print('Upload files done.')

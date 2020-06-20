from config import EXCHANGE_TOPIC, TOPIC_DOWNLOAD
from .publisher import PublisherService

import pika
import requests

PATH_DOWNLOADED_FILE = './temp/downloader'

SUPPORTED_CONTENT_TYPE = {
    'txt','png','jpg','jpeg','mp4','mp3'
}

EXCHANGE_NAME_PUBLISH = EXCHANGE_TOPIC
EXCHANGE_TYPE_PUBLISH = 'topic'

class DownloadService:
    def __init__(self):
        self.publisher = PublisherService(exchange_name=EXCHANGE_NAME_PUBLISH, exchange_type=EXCHANGE_TYPE_PUBLISH)

    def send_progress(self, filename, progress, status):
        payload = {
            'file_id':filename,
            'progress':progress,
            'status':status
        }
        
        self.publisher.send_msg_to_rk(rk=TOPIC_DOWNLOAD, msg=payload)
        print(f' Sent progress! Download: {filename}; progress: {progress}; status: {status}')
    
    def get_extension(self, url):
        filename = url.split('/')[-1]
        ext = filename.split('.')[-1]
        if ext in SUPPORTED_CONTENT_TYPE:
            return ext
        return SUPPORTED_CONTENT_TYPE[0]

    def download(self, filename, url):
        filename_ext = f'{filename}.{self.get_extension(url)}'
        file_path = f'{PATH_DOWNLOADED_FILE}/{filename_ext}'
        
        with open(file_path, "wb") as f:
            print(f'Start downloading {filename_ext}...')
            response = requests.get(url, stream=True)
            
            total_length = response.headers.get('content-length')
            status = False

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                data_length = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    data_length += len(data)
                    f.write(data)
                    
                    percentage = int((data_length / total_length) * 100)
                    if percentage >= 100:
                        status = True

                    self.send_progress(filename=filename, progress=f'{percentage}%', status=status)
        return filename_ext
        
                    

    def bulk_download(self, file_url_dict):
        file_id_name = {}
        for fn in file_url_dict:
            file_id_name[fn] = self.download(filename=fn, url=file_url_dict[fn])
        print(f'Download files done. Downloaded: {file_id_name}')
        return file_id_name

import base64
import hashlib
import calendar
import datetime

def encode_bytes_str(data_bytes):
    return base64.b64encode(data_bytes).decode('utf-8')

def decode_b64str_bytes(data):
    data_bytes = data.encode('utf-8')
    return base64.b64decode(data_bytes)

def get_secured_link(filename):
    URL_BASE = 'http://localhost:5004/files'
    SECRET_KEY = 'secret'
    
    # in EPOCH format
    future = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    expire = calendar.timegm(future.timetuple())

    secure_link = f"{expire} {SECRET_KEY}".encode('utf-8')
    hashmd5 = hashlib.md5(secure_link).digest()
    base64_hash = base64.urlsafe_b64encode(hashmd5)
    str_hash = base64_hash.decode('utf-8').rstrip('=')

    return f"{URL_BASE}?md5={str_hash}&expires={expire}&filename={filename}"

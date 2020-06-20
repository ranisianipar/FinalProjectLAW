# Test Kit

### Valid URL Input
```python
url_large = 'https://storage.googleapis.com/meirtvmp3/archive/hebrew/mp3/sherki/daattvunot/idx_69115.mp3'
url_small = 'https://www.python.org/static/img/python-logo@2x.png'
```

### Link to Download Compressed Folder
- Valid: 
http://localhost:5004/files?md5=8Y0_l0Ql2vSGKAW8S1_iPw&expires=2147483647&filename=<input>

- Invalid: 
http://localhost:5004/files?md5=RANDOMRANDOM&expires=2147483647&filename=<input>

- Expired: 
http://localhost:5004/files?md5=Ff37Lg8OcyDePLW_F71DRQ&expires=1592384038&filename=<input>


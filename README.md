# tornado-file-handling
:wrench: Playing around with Tornado file handling

## Run
```bash
virtualenv -p python3 venv
pip3 install -r requirements.txt
python3 server.py
```

## Usage
Upload file (multipart):  
```
POST /api/file HTTP/1.1
Host: localhost:8888
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

(data)
----WebKitFormBoundary7MA4YWxkTrZu0gW
```
  
List files:  
```
GET /api/file HTTP/1.1
Host: localhost:8888
```

Get file:  
```
GET /api/file?filename=test.txt HTTP/1.1
Host: localhost:8888
```
  
Delete file:  
```
DELETE /api/file?filename=test.txt HTTP/1.1
Host: localhost:8888
```

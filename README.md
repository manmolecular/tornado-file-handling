# tornado-file-handling
Playing around with Tornado and file handling

## Run
```bash
virtualenv -p python3 venv
pip3 install -r requirements.txt
python3 server.py
```

## Usage
Upload file:  
```bash
GET /api/file HTTP/1.1
Host: localhost:8888
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="example.png"
Content-Type: <Content-Type header here>

(data)
----WebKitFormBoundary7MA4YWxkTrZu0gW
```
  
List files:  
```bash
GET /api/file HTTP/1.1
Host: localhost:8888
```

Get file:  
```bash
GET /api/file?filename=example.png HTTP/1.1
Host: localhost:8888
```
  
Delete file:  
```bash
DELETE /api/file?filename=example.png HTTP/1.1
Host: localhost:8888
```

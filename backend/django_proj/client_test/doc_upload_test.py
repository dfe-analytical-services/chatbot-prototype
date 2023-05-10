import requests
import os
import mimetypes




endpoint = 'http://localhost:8000/doc_parse/'
doc_path = 'sample.pdf'

with open(doc_path, 'rb') as f:
    file_name = doc_path
    file_size = os.path.getsize(doc_path)
    content_type = mimetypes.guess_type(doc_path)[0]
    
    data = {
        'file_name':file_name,
        'file_size':file_size,
        'content_type': content_type
    }
    files = {"file": (file_name, f)}
    response = requests.post(endpoint, files = files, data = data)
    
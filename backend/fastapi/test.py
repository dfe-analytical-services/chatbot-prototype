import requests
import json

# URL of your FastAPI app
url = 'http://localhost:8000/api'

# The payload for your request
payload = {
    "question": "Hi how are you?"
}

# headers for a JSON request
headers = {
    'Content-Type': 'application/json',
}

# Make the POST request
response = requests.post(url, data=json.dumps(payload), headers=headers, stream=True)

# Verify that the response is streamed

# Print each chunk of the response
for chunk in response.iter_content(decode_unicode=True):
    if chunk:  # filter out keep-alive new chunks
        print(chunk)


import requests

endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint, json={'question': 'what ya name', 'history':[]}, headers={
    "Content-Type": "application/json", 
    'X-Session-ID': '13ehrhfdjnc211'})

print(get_response.json())

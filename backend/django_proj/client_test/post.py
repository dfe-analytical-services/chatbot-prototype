import requests
import traceback

endpoint = "http://localhost:8000/api/"


try:
    get_response = requests.post(endpoint, json={'question': 'How many edtech companies are there', 'history':[], 
                                             'sessionId': 'jdndc30382',
                                             'documentId': 'namespace_8'})

    json = get_response.json()
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except requests.exceptions.RequestException as req_err:
    print(f'Request error occurred: {req_err}')
    print(traceback.format_exc())
except ValueError as val_err:
    print(f'ValueError occurred: {val_err}')
    print(f'Response content: {get_response.text}')

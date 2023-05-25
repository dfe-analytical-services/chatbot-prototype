import requests
import traceback

endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint, json={'question': 'What is this report about', 'history':[], 
                                             'sessionId': 'jdndc30382',
                                             'documentId': 'namespace_17'
                                             })

print(get_response.json())


